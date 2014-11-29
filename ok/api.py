#!env python2
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

# load the user configured functions
APP_NAME = "ok"
CONFIG_DIR = xdg.BaseDirectory.save_config_path(APP_NAME)
DATA_DIR = xdg.BaseDirectory.save_data_path(APP_NAME)
sys.path.append(CONFIG_DIR)
try:
    import config
except ImportError:
    pass

USERS_DB_PATH = os.path.join(DATA_DIR, "users.kch")
USERS_DB = serializeddicts.KyotoCabinetDict(USERS_DB_PATH)
GROUPS_FILE = os.path.join(CONFIG_DIR, "groups.json")
GROUPS = { "users" : {} }

def save_groups():
    """
    saves the groups in the dedicated file
    """
    with open(GROUPS_FILE, "wb") as f:
        json.dump(GROUPS, indent=4, fp=f)

# load the groups and their restrictions
if os.path.exists(GROUPS_FILE):
    with open(GROUPS_FILE) as f:
        GROUPS = json.load(f)
else:
    # create the file if it does not exist, reset the admin group to avoid
    # problems
    GROUPS["admin"] = { "/.*$" : [ [ "unrestricted", None ] ] }
    save_groups()

def urldecode(s):
    return urllib2.unquote(s).decode('utf-8')

def json_response(status, body={}):
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
        body = { "message": body }
    body["status"] = status_message[status]
    response = flask.jsonify(body)
    response.status = str(status)
    return response

def describe_rights(groups):
    return {}

@app.route("/ok/")
def ok():
    """
    Description:
    This resource represents the fact that the described request is
    allowed or not.

    How to query:
    GET /ok/?url=<url>&user=<user>&groups=<group-list>&http_method=<http_method>&post_parameters=<post_parameters>

    Arguments:
    - url (mandatory):
    The full url of the http request
    - http_method (optional):
    The http method used (defaults to GET)
    - user (optional):
    The user who attempts to access the url
    - groups (optional)
    The groups the user belong to, separated by commas
    - post_parameters (optional)
    The post parameters (data type application/x-www-form-urlencoded)

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

    url = flask.request.args.get("url", None)
    groups = flask.request.args.get("groups", None)
    user = flask.request.args.get("user", None)
    http_method = urldecode(flask.request.args.get("http_method", "GET"))
    post_parameters = flask.request.args.get("post_parameters", None)

    if not url:
        return json_response(400, "Expected a url argument")
    if not (user or groups):
        return json_response(400, "Expected a user or some groups")
    if user:
        user = urldecode(user)
    if user and not USERS_DB.get(user):
        return json_response(400, "User %s does not exist" % user)
    if groups:
        try:
            groups = urldecode(groups).split(",")
        except TypeError:
            return json_response(400, "Could not parse the groups")
    else:
        groups = USERS_DB[user]["groups"]
    if post_parameters:
        try:
            post_parameters = urllib.parse_qs(post_parameters)
        except ValueError:
            return json_response(
                    400,
                    "Could not parse post_parameters %s" % post_parameters
                    )
    for group in groups:
        if not GROUPS.get(group):
            return json_response(404, "Group %s does not exist" % group)

    url_parts = urlparse.urlsplit(url)

    http_scheme = url_parts.scheme
    http_netloc = url_parts.netloc
    http_path = url_parts.path
    http_query = url_parts.query
    http_fragment = url_parts.fragment # should always be None
    http_username = url_parts.username
    http_password = url_parts.password
    http_hostname = url_parts.hostname
    http_port = url_parts.port

    if http_query:
        try:
            http_query = urlparse.parse_qs(url_parts.query)
        except ValueError:
            return json_response(
                    400, "Could not parse http_query %s" % http_query
                    )

    # For each groups, we go through all the path patterns.
    for group in groups:
        restrictions = GROUPS[group]
        match_found = False
        # All the matching patterns must return True if the path matches
        for path_pattern, restriction_list in restrictions.iteritems():
            if re.match(path_pattern, http_path):
                match_found = True
                for restrictionname, restriction_params in restriction_list:
                    try:
                        rule = restrictions_manager.get(restrictionname)
                    except KeyError:
                        return json_response(
                                500,
                                "%s: unknown restriction" % restrictionname
                                )
                    if not rule.applies(
                            groupname=group,
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
                            post_parameters=post_parameters,
                            restriction_params=restriction_params
                            ):
                        return json_response(403, "Restriction %s on %s"
                                % (restrictionname, path_pattern))
        # We need to find at least one matching path
        if match_found:
            return json_response(200, describe_rights(groups))

    return json_response(403, "Not allowed (no matching path on any group)")

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

    Returns:

    Additional details:
    """
    # list all users
    if username is None:
        return flask.jsonify(USERS_DB)
    else:
        user = USERS_DB.get(username)
        if flask.request.method == "GET":
            if user is None:
                return json_response(404, "Unknown user")
            else:
                return flask.jsonify(user)
        if flask.request.method in ("POST", "PUT"):
            try:
                groups = flask.request.form.get("groups", "users")
                groups = set(groups.split(","))
            except TypeError:
                return json_response(400, "Could not parse groups")
            # create the group if it does not exist
            for group in groups:
                if group not in GROUPS:
                    GROUPS[group] = {}
                    save_groups()
            # any user is part of the group "users"
            groups.add("users")
            USERS_DB [username] = { "groups": list(groups) }
            return json_response(200, "User created or updated")
        if flask.request.method == "DELETE":
            if user is None:
                return json_response(404, "%s: unknown user" % username)
            del USERS_DB[username]
            return json_response(204, "/users/%s deleted" % username)

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
    DELETE /GROUPS/<groupname>

    Returns:

    Additional details:
    """
    if groupname is None:
        return flask.jsonify(GROUPS)
    else:
        group = GROUPS.get(groupname)
        if flask.request.method == "GET":
            if group is None:
                return json_response(404, "%s: unknown group" % groupname)
            else:
                return flask.jsonify(group)
        if flask.request.method in ("POST", "PUT"):
            try:
                posted_restrictions = flask.request.form.get("restrictions")
                if not posted_restrictions:
                    restrictions = {}
                else:
                    restrictions = dict(
                            json.loads(urldecode(posted_restrictions))
                            )
            except TypeError:
                return json_response(
                        400, "Could not parse provided restrictions %s" %
                        posted_restrictions
                        )
            for path_pattern, restriction_list in restrictions.iteritems():
                for restrictionname, restriction_params in restriction_list:
                    if restrictionname not in restrictions_manager.all():
                        return json_response(
                                404, "%s: unknown restriction" %
                                restrictionname
                                )
            GROUPS[groupname] = restrictions
            save_groups()
            return json_response(
                    200, "Created or updated the group %s" % groupname
                    )
        if flask.request.method == "DELETE":
            if group is None:
                return json_response(404, "%s: unknown group" % groupname)
            del GROUPS[groupname]
            save_groups()
            for username, groups in USERS_DB.iteritems():
                if groupname in groups["groups"]:
                    groups["groups"].remove(groupname)
                    USERS_DB[username] = groups
            return json_response(204, "/groups/%s deleted" % groupname)

@app.route("/restrictions/")
@app.route("/restrictions/<restrictionname>")
def restrictions(restrictionname=None):
    """
    Description:
    This resource represents the restrictions apliable to requests

    How to query:
    GET /restrictions
    GET /restrictions/<restrictionname>

    Returns:

    Additional details:
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
            return json_response(200, { "description" : description })

@app.route("/")
@app.route("/app_info")
def app_info():
    res = dict()
    res["USERS_DB_PATH"] = USERS_DB_PATH
    res["GROUPS_FILE"] = GROUPS_FILE
    res["CONFIG_FILE"] = os.path.join(CONFIG_DIR, "config.py")
    res["links"] = "/help/"
    return flask.jsonify(res)

@app.route("/help/")
@app.route("/help/<endpoint>")
def help(endpoint=None):
    """Help for the developers"""
    if endpoint is None:
        all_endpoints = [ rule.endpoint for rule in
                app.url_map.iter_rules() if rule.endpoint != "static" ]
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
