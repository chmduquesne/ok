# -*- coding: utf-8 -*-

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
import werkzeug.datastructures
import itertools

from restrictions import restrictions_manager
from ok import app

APP_NAME = "ok"
XDG_CONFIG_DIR = xdg.BaseDirectory.save_config_path(APP_NAME)
XDG_DATA_DIR = xdg.BaseDirectory.save_data_path(APP_NAME)

app.config.update(dict(
    USERS_DB=os.path.join(XDG_DATA_DIR, "users.kch"),
    GROUPS_DB=os.path.join(XDG_CONFIG_DIR, "groups.json"),
    AUTO_CREATE=True,
    DEFAULT_GROUPS=["users"],
    ANONYMOUS_GROUPS=["anonymous"],
    MAX_RESULTS=20
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
            raise RuntimeError("Could not import config from %s" %
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
        groups_db["unrestricted"] = {
            "hint": True,
            "restrictions": [[".*", "unrestricted", None]]
            }
        for groupname in app.config["DEFAULT_GROUPS"]:
            if groupname not in groups_db:
                groups_db[groupname] = {"hint": True, "restrictions": []}
        for groupname in app.config["ANONYMOUS_GROUPS"]:
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
    if status != 200:
        body["status"] = status_message[status]
        body["status_code"] = status
    response = flask.jsonify(body)
    response.status = str(status)
    return response


def describe(group_list):
    """
    Describes the groups with their hints (will raise an exception if the
    groups database in not correct)
    """
    groups_db = get_groups_db()
    return dict(((groupname, groups_db[groupname]["hint"])
                for groupname in group_list))


def parse_qs(qs, keep_blank_values=False, strict_parsing=False):
    """
    parse query string into a werkzeug MultiDict
    """
    return werkzeug.datastructures.MultiDict(
        urlparse.parse_qs(qs, keep_blank_values, strict_parsing)
        )


def create_user_if_not_exists(username):
    users_db = get_users_db()

    if username not in users_db:
        return post_user(username, group_list=app.config["DEFAULT_GROUPS"])


def url_input_groups():
    users_db = get_users_db()

    res = app.config["ANONYMOUS_GROUPS"]
    if "groups" in flask.request.args:
        res = flask.request.args["groups"].split(",")
    else:
        if "user" in flask.request.args:
            username = flask.request.args["user"]
            if username in users_db:
                res = users_db[username]["groups"]
    return res


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

    if "user" in flask.request.args:
        if app.config["AUTO_CREATE"]:
            create_user_if_not_exists(flask.request.args["user"])

    group_list = url_input_groups()

    data = werkzeug.datastructures.MultiDict()
    if "data" in flask.request.args:
        data = parse_qs(flask.request.args["data"])

    http_method = flask.request.args.get("http_method")

    # At this point, we know we have a request and some groups.
    url_parts = urlparse.urlsplit(flask.request.args["url"])

    http_scheme = url_parts.scheme
    http_netloc = url_parts.netloc
    http_path = url_parts.path
    http_fragment = url_parts.fragment  # should always be None
    http_username = url_parts.username
    http_password = url_parts.password
    http_hostname = url_parts.hostname
    http_port = url_parts.port

    http_query = werkzeug.datastructures.MultiDict()
    if url_parts.query is not None:
        http_query = parse_qs(url_parts.query)

    # We process it through the restrictions of each group

    match_found = False
    for groupname in itertools.ifilter(lambda g: g in groups_db, group_list):
        restriction_list = groups_db[groupname]["restrictions"]
        for path_pattern, restrictionname, restriction_params \
                in restriction_list:
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

        if match_found:
            return json_response(200, describe(group_list))

    return json_response(403, "Not allowed")


def requested_page():
    res = 1
    if "page" in flask.request.args:
        try:
            res = int(flask.request.args["page"])
        except ValueError:
            res = 1
    return res


def page(n):
    return n // app.config["MAX_RESULTS"] + 1


def get_users(s="", p=1):
    users_db = get_users_db()

    res = {"users": {}}
    search_func = lambda x: s in x[0]
    for n, (username, userdata) in enumerate(
            itertools.ifilter(search_func, users_db.iteritems())):
        if page(n) == p:
            res["users"][username] = userdata
    res["page"] = p
    if s == "":
        res["total_pages"] = page(len(users_db))

    return flask.jsonify(res)


def get_user(username):
    users_db = get_users_db()

    if username not in users_db:
        return json_response(404, {
            "message": "%s: unknown user" % username
            })
    else:
        return flask.jsonify(users_db[username])


def form_input_groups():
    res = []
    try:
        res = flask.request.form["groups"].split(",")
    except KeyError:
        res = app.config["DEFAULT_GROUPS"]
    return res


def post_user(username, group_list=[]):
    users_db = get_users_db()

    if username in users_db:
        return json_response(400, "%s: user already exists")

    users_db[username] = {"groups": group_list}

    return json_response(201, {
        "message": "%s: user created" % username,
        })


def put_user(username, group_list=[]):
    users_db = get_users_db()

    if username not in users_db:
        return json_response(404, "%s: unknown user")

    users_db[username] = {"groups": group_list}

    return json_response(200, {
        "message": "%s: user updated" % username,
        })


def delete_user(username):
    users_db = get_users_db()

    if username not in users_db:
        return json_response(404, "%s: unknown user" % username)
    res = {
            "message": "user %s deleted" % username,
            "data": users_db[username],
            "username": username,
            }
    del users_db[username]
    return json_response(200, res)


@app.route("/users/")
@app.route("/users/<username>", methods=["GET", "POST", "DELETE", "PUT"])
def users(username=None):
    """
    Description:
    This resource represents the users

    How to query:
    GET /users/
    GET /users/?page=2
    GET /users/bob?as_filter=1
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

    if flask.request.method == "GET":
        p = requested_page()
        search = username
        if username is None:
            search = ""
        if username is None or "as_filter" in flask.request.args:
            return get_users(search, p)
        return get_user(username)

    if flask.request.method == "POST":
        group_list = form_input_groups()
        return post_user(username, group_list)

    if flask.request.method == "PUT":
        group_list = form_input_groups()
        return put_user(username, group_list)

    if flask.request.method == "DELETE":
        return delete_user(username)


def get_all_groups():
    groups_db = get_groups_db()

    res = {"groups": {}}
    for groupname, groupdata in groups_db.iteritems():
        res["groups"][groupname] = groupdata

    return flask.jsonify(res)


def get_group(groupname):
    groups_db = get_groups_db()

    if groupname not in groups_db:
        return json_response(404, "%s: unknown group" % groupname)
    else:
        return flask.jsonify(groups_db[groupname])


def form_input_restriction_list(groupname):
    groups_db = get_groups_db()

    res = []
    if groupname in groups_db:
        res = groups_db[groupname]["restrictions"]
    if "restrictions" in flask.request.form:
        res = json.loads(flask.request.form["restrictions"])
    return res


def form_input_hint(groupname):
    groups_db = get_groups_db()

    res = True
    if groupname in groups_db:
        res = groups_db[groupname]["hint"]
    if "hint" in flask.request.form:
        res = json.loads(flask.request.form["hint"])
    return res


def check_restriction_list(restriction_list):
    for rule in restriction_list:
        if not isinstance(rule, list):
            return False
        if not len(rule) == 3:
            return False
        if not isinstance(rule[0], basestring):
            return False
        if not isinstance(rule[1], basestring):
            return False
        if not rule[1] in restrictions_manager:
            return False
    return True


def post_group(groupname, hint=True, restriction_list=[]):
    groups_db = get_groups_db()

    if groupname in groups_db:
        return json_response(400, "%s: group already exists")

    groups_db[groupname] = {
        "hint": hint,
        "restrictions": restriction_list
        }
    return json_response(
        201, "%s: group created" % groupname
        )


def put_group(groupname, hint=True, restriction_list=[]):
    groups_db = get_groups_db()

    if groupname not in groups_db:
        return json_response(404, "%s: unknown group")

    groups_db[groupname] = {
        "hint": hint,
        "restrictions": restriction_list
        }

    return json_response(
        200, "%s: group updated" % groupname
        )


def delete_group(groupname):
    groups_db = get_groups_db()

    if groupname not in groups_db:
        return json_response(404, "%s: unknown group" % groupname)
    res = {
            "message": "group %s deleted" % groupname,
            "data": groups_db[groupname],
            "groupname": groupname,
            }
    del groups_db[groupname]
    return json_response(200, res)


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
    if flask.request.method == "GET":
        if groupname is None:
            return get_all_groups()
        else:
            return get_group(groupname)

    if flask.request.method == "POST":
        restriction_list = form_input_restriction_list(groupname)
        hint = form_input_hint(groupname)
        if not check_restriction_list(restriction_list):
            return json_response(400, "%s: invalid restrictions" %
                    restriction_list)
        return post_group(groupname, hint, restriction_list)

    if flask.request.method == "PUT":
        restriction_list = form_input_restriction_list(groupname)
        hint = form_input_hint(groupname)
        if not check_restriction_list(restriction_list):
            return json_response(400, "%s: invalid restrictions" %
                    restriction_list)
        return put_group(groupname, hint, restriction_list)

    if flask.request.method == "DELETE":
        return delete_group(groupname)


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
        res = {"restrictions": {}}
        for restrictionname, restrictiondata in restrictions_manager.all().iteritems():
            res["restrictions"][restrictionname] = restrictiondata
        return flask.jsonify(res)
    else:
        description = restrictions_manager.all().get(restrictionname)
        if description is None:
            return json_response(
                404, "%s: unknown restriction" % restrictionname
                )
        else:
            return json_response(200, {"description": description})


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
                         app.url_map.iter_rules()
                         if rule.endpoint != "static" and rule.endpoint != "root"]
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


@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.after_request
def debug_cache_off(response):
    if app.config["DEBUG"]:
        response.headers["Cache-Control"] = "no-cache, max-age=0"
    return response
