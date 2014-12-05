# -*- coding: utf-8 -*-

from __future__ import with_statement
import urlparse
import urllib2
import flask
import xdg.BaseDirectory
import os
import sys
import json
import re
import serializeddicts

from restrictions import restrictions_manager
from ok import app

APP_NAME = "ok"
XDG_CONFIG_DIR = xdg.BaseDirectory.save_config_path(APP_NAME)
XDG_DATA_DIR = xdg.BaseDirectory.save_data_path(APP_NAME)

app.config.update(dict(
    USERS_DB=os.path.join(XDG_DATA_DIR, "users.kch"),
    GROUPS_DB=os.path.join(XDG_CONFIG_DIR, "groups.json"),
    AUTO_CREATE=True,
    DEFAULT_GROUPS=["users"]
    ))


def load_config_from_envvar(varname, silent=True):
    """
    This function replaces app.config.from_envvar

    The reason why it was written was to allow references to allow actual
    import of the user code in the config. app.config.from_envvar is too
    limited in that regards, and functions that references to local
    variables within the file would be otherwise lost.
    """
    config_path = os.getenv(varname)
    if config_path is None or not os.path.exists(config_path):
        if silent:
            return
        else:
            raise RuntimeError("No configuration in the variable %s" %
                    varname)
    dirname = os.path.dirname(config_path)
    pyfile = os.path.basename(config_path)
    modulename = os.path.splitext(pyfile)[0]
    syspath = list(sys.path)
    try:
        sys.path.insert(0, dirname)
        config = __import__(modulename)
        for attr in dir(config):
            if attr.isupper():
                app.config[attr] = getattr(config, attr)
    finally:
        sys.path[:] = syspath

load_config_from_envvar("OK_CONFIG", silent=True)


def get_groups_db():
    """
    Returns the group database from the application context (creates it if
    necessary).
    """
    if not hasattr(flask.g, "groups_db"):
        groups_db = serializeddicts.JsonDict(app.config["GROUPS_DB"])
        groups_db["unrestricted_users"] = {
                "hint": True,
                "restrictions": [[".*", "unrestricted", None]]
                }
        for groupname in app.config["DEFAULT_GROUPS"]:
            if groupname not in groups_db:
                groups_db[groupname] = {"hint": True, "restrictions": []}
        flask.g.groups_db = groups_db
    return flask.g.groups_db


def get_users_db():
    """
    Returns the users database from the application context (creates it if
    necessary).
    """
    if not hasattr(flask.g, "users_db"):
        flask.g.users_db = serializeddicts.KyotoCabinetDict(
            app.config["USERS_DB"]
            )
    return flask.g.users_db


def json_response(status, body={}):
    """
    Builds a response object with the content type set to json
    """
    status_message = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not found",
        413: "Request entity too large",
        429: "Too many requests",
        500: "Internal error"
        }
    if not isinstance(body, dict):
        body = {"message": body}
    body["status"] = status_message[status]
    response = flask.jsonify(body)
    response.status = str(status)
    return response


def describe(group_list):
    """
    Describes the groups with their hints (will raise an exception if the
    groups database in not correct)
    """
    groups_db = get_groups_db()
    return dict(((groupname, groups_db[groupname]["hint"]) for groupname in group_list))


@app.route("/ok/")
def ok():
    """
    Description:
    This resource represents the fact that the described request is
    allowed or not.

    How to query:
    GET /ok/?url=<url>&user=<user>&groups=<group-list>&http_method=<http_method>&data=<data>

    Arguments:
    - url (mandatory):
    The full url of the http request
    - http_method (optional):
    The http method used (defaults to GET)
    - user (optional):
    The user who attempts to access the url
    - groups (optional)
    The groups the user belong to, separated by commas
    - data (optional)
    The post/put data (assuming type application/x-www-form-urlencoded)

    All the arguments must be url-encoded. One of the parameters user or
    groups must be provided. If both are provided, the api call will
    ignore the user argument.

    Returns:
    - A 400 Error if the request was incorrectly described
    - A 404 Error if the user or the groups do not exist
    - A 403 Error if the request is forbidden
    - A 200 Status if the request is valid

    Additionally to the http status, a message is returned detailing the
    problem in case of error. If the request is valid, a message
    describing the user rights is returned.

    How it works:
    - a user belongs to groups
    - groups are subject to restrictions
    If one of the groups is allowed to execute the request, then this
    request is considered valid. A group is allowed to execute a request
    if all the restrictions on this request are satisfied.

    Additional details:
    There is no way to apply restrictions to a specific user, it has to be
    done through a group. This is a design decision intended to avoid
    doing a user lookup for every request where the groups were provided.
    The workaround, if you want to give special rights to a user, create a
    group specifically for this user.
    """
    users_db = get_users_db()
    groups_db = get_groups_db()

    if "url" not in flask.request.args:
        return json_response(400, "Expected a url argument")
    if "user" not in flask.request.args and "groups" not in flask.request.args:
        return json_response(400, "Expected a user or some groups")
    if "groups" not in flask.request.args:
        username = flask.request.args["user"]
        if not users_db.get(username):
            if app.config["AUTO_CREATE"]:
                users_db[username] = {
                    "groups": app.config["DEFAULT_GROUPS"]
                    }
            else:
                return json_response(403, "%s: unkown user" % username)
        group_list = users_db[username]["groups"]
    else:
        try:
            group_list = flask.request.args["groups"].split(",")
        except TypeError:
            return json_response(400, "%s: unparsable groups" % groups_arg)
    data = {}
    if "data" in flask.request.args:
        try:
            data = urllib.parse_qs(flask.request.args["data"])
        except ValueError:
            return json_response(
                400,
                "%s: unparsable data" % data_arg
                )
    http_method = flask.request.args.get("http_method")
    for group in group_list:
        if groups_db.get(group) is None:
            return json_response(403, "%s: unknown group" % group)

    url_parts = urlparse.urlsplit(flask.request.args["url"])

    http_scheme = url_parts.scheme
    http_netloc = url_parts.netloc
    http_path = url_parts.path
    http_query = url_parts.query
    http_fragment = url_parts.fragment  # should always be None
    http_username = url_parts.username
    http_password = url_parts.password
    http_hostname = url_parts.hostname
    http_port = url_parts.port

    if http_query is not None:
        try:
            http_query = urlparse.parse_qs(url_parts.query)
        except ValueError:
            return json_response(
                400, "%s: unparsable http_query" % http_query
                )

    match_found = False
    # For each groups, we go through all the path patterns.
    for groupname in group_list:
        try:
            restriction_list = groups_db[groupname]["restrictions"]
            # All the matching patterns must return True if the path matches
            for path_pattern, restrictionname, restriction_params in restriction_list:
                if re.match(path_pattern, http_path):
                    match_found = True
                    rule = restrictions_manager.get(restrictionname)
                    if not rule.applies(
                            groupname=groupname,
                            http_scheme=http_scheme,
                            http_netloc=http_netloc,
                            http_path=http_path,
                            http_query=http_query,
                            http_fragment=http_fragment,
                            http_username=http_username,
                            http_password=http_password,
                            http_hostname=http_hostname,
                            http_port=http_port,
                            http_method=http_method,
                            http_data=data,
                            restriction_params=restriction_params
                            ):
                        match_found = False
                        break
        except (KeyError, TypeError, ValueError):
            return json_response(
                500,
                "%s: group incorrectly defined" % groupname
                )

        # We need to find at least one matching path
        if match_found:
            return json_response(200, describe(group_list))

    return json_response(403, "Not allowed")


@app.route("/users/")
@app.route("/users/<username>", methods=["GET", "POST", "DELETE", "PUT"])
def users(username=None):
    """
    Description:
    This resource represents the users

    How to query:
    GET /users
    GET /users/<username>
    POST /users/<username>
    PUT /users/<username>
    DELETE /users/<username>

    Data Model:
    users = {
        username1: {
           "groups": ["groupname1", "groupname2", ...]
        },
        username2: {
           "groups": ["groupname1", "groupname2", ...]
        },
        ...
    }
    """
    # list all users
    users_db = get_users_db()

    if username is None:
        return flask.jsonify(users_db)
    else:
        if flask.request.method == "GET":
            if username not in users_db:
                return json_response(404, "%s: unknown user" % username)
            else:
                return flask.jsonify(users_db[username])

        if flask.request.method in ("POST", "PUT"):

            if flask.request.method == "POST":
                if username in users_db:
                    return json_response(400, "%s: user already exists")
            if flask.request.method == "PUT":
                if username not in users_db:
                    return json_response(404, "%s: unknown user")

            try:
                group_list = flask.request.form["groups"].split(",")
            except KeyError:
                group_list = []

            for groupname in app.config["DEFAULT_GROUPS"]:
                if groupname not in group_list:
                    group_list.append(groupname)

            groups_db = get_groups_db()
            for groupname in group_list:
                if groupname not in groups_db:
                    if app.config["AUTO_CREATE"]:
                        groups_db[groupname] = {}
                    else:
                        return json_response(404, "%s: unknown group" %
                                             groupname)

            users_db[username] = {"groups": group_list}

            if flask.request.method == "POST":
                return json_response(201, "%s: user created" % username)
            else:
                return json_response(200, "%s: user updated" % username)

        if flask.request.method == "DELETE":
            if username not in users_db:
                return json_response(404, "%s: unknown user" % username)
            del users_db[username]
            return json_response(200, "/users/%s deleted" % username)


@app.route("/groups/")
@app.route("/groups/<groupname>", methods=["GET", "POST", "DELETE", "PUT"])
def groups(groupname=None):
    """
    Description:
    This resource represents the groups

    How to query:
    GET /groups
    GET /groups/<groupname>
    POST /groups/<groupname>
    PUT /groups/<groupname>
    DELETE /groups/<groupname>

    Data Model:
    groups = {
        groupname1: {
            "hint" : <json to forward to the webservice in case of success>,
            "restrictions": [
                ["path_pattern1", "restrictionname1", parameters1],
                ["path_pattern2", "restrictionname2", parameters2],
                ...
            ]
        },
        groupname2: {
            "hint" : <json to forward to the webservice in case of success>,
            "restrictions": [
                ["path_pattern1", "restrictionname1", parameters1],
                ["path_pattern2", "restrictionname2", parameters2],
                ...
            ]
        },
        ...
    }
    """
    groups_db = get_groups_db()

    if groupname is None:
        return flask.jsonify(groups_db)
    else:
        if flask.request.method == "GET":
            if groupname not in groups_db:
                return json_response(404, "%s: unknown group" % groupname)
            else:
                return flask.jsonify(groups_db[groupname])

        if flask.request.method in ("POST", "PUT"):

            if flask.request.method == "POST":
                if groupname in groups_db:
                    return json_response(400, "%s: group already exists")
            if flask.request.method == "PUT":
                if groupname not in groups_db:
                    return json_response(404, "%s: unknown group")

            try:
                restrictions_arg = flask.request.form.get("restrictions", None)
                if restrictions_arg is None:
                    path_restrictions = {
                            "hint": True,
                            "restrictions": []
                            }
                else:
                    path_restrictions = dict(
                        json.loads(restrictions_arg)
                        )
                if "hint" not in path_restrictions:
                    path_restrictions["hint"] = True
                for path_pattern, restrictionname, restriction_params in \
                        path_restrictions["restrictions"]:
                    if restrictionname not in restrictions_manager.all():
                        return json_response(
                            404, "%s: unknown restriction" %
                            restrictionname
                            )
            except (KeyError, TypeError, ValueError):
                return json_response(
                    400, "%s: Could not parse provided restrictions" %
                    restrictions_arg
                    )

            groups_db[groupname] = path_restrictions

            if flask.request.method == "POST":
                return json_response(
                    201, "%s: group created" % groupname
                    )
            if flask.request.method == "PUT":
                return json_response(
                    200, "%s: group updated" % groupname
                    )
        if flask.request.method == "DELETE":
            if groupname not in groups_db:
                return json_response(404, "%s: unknown group" % groupname)
            del groups_db[groupname]
            users_db = get_users_db()
            for username, groups in users_db.iteritems():
                if groupname in groups["groups"]:
                    groups["groups"].remove(groupname)
                    users_db[username] = groups
            return json_response(200, "/groups/%s deleted" % groupname)


@app.route("/restrictions/")
@app.route("/restrictions/<restrictionname>")
def restrictions(restrictionname=None):
    """
    Description:
    This resource represents the restrictions apliable to requests

    How to query:
    GET /restrictions
    GET /restrictions/<restrictionname>
    """
    if restrictionname is None:
        return flask.jsonify(restrictions_manager.all())
    else:
        description = restrictions_manager.all().get(restrictionname)
        if description is None:
            return json_response(
                404, "%s: unknown restriction" % restrictionname
                )
        else:
            return json_response(200, {"description": description})


@app.route("/")
@app.route("/config/")
def config():
    """
    Description:
    This resource gives you info about how the app is configured
    """
    res = dict()
    res["USERS_DB"] = app.config["USERS_DB"]
    res["GROUPS_DB"] = app.config["GROUPS_DB"]
    res["links"] = "/help/"
    return flask.jsonify(res)


@app.route("/help/")
@app.route("/help/<endpoint>")
def help(endpoint=None):
    """
    Description:
    This resource prints help for the developers
    """
    if endpoint is None:
        all_endpoints = [rule.endpoint for rule in
                         app.url_map.iter_rules() if rule.endpoint != "static"]
        links = dict()
        for e in all_endpoints:
            links[e] = "/help/%s" % e
        return json_response(200, {"links": links})
    else:
        func = app.view_functions.get(endpoint, None)
    if not func:
        return json_response(404, "%s: unkown endpoint" % str(endpoint))
    if not func.__doc__:
        return json_response(404, "%s: no documentation" % str(endpoint))
    response = flask.make_response(func.__doc__)
    response.headers["Content-Type"] = "text/plain"
    return response
