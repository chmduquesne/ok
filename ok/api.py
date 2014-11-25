#!env python2
import urlparse
import urllib2
import flask
import xdg.BaseDirectory
import os
import sys
import json
import re

from kyotocabinetdict import KyotoCabinetDict
from restrictions import restrictions_manager
from ok import app

# load the user configured functions
APP_NAME = "ok"
CONFIG_DIR = xdg.BaseDirectory.save_config_path(APP_NAME)
USERS_DB_PATH = os.path.join(xdg.BaseDirectory.save_data_path(APP_NAME), "users.kch")
GROUPS_DB_PATH = os.path.join(xdg.BaseDirectory.save_data_path(APP_NAME), "groups.kch")
sys.path.append(CONFIG_DIR)
try:
    import config
except ImportError:
    pass

USERS_DB = KyotoCabinetDict(USERS_DB_PATH)
GROUPS_DB = KyotoCabinetDict(GROUPS_DB_PATH)

def urldecode(s):
    return urllib2.unquote(s).decode('utf-8')

def make_json_response(message, status="200"):
    response = flask.jsonify({"message": message})
    response.status = status
    return response

def describe_user(user):
    return {}

@app.route("/ok/")
def ok():
    """
    Description:
    This api call checks whether the provided request is allowed or not.

    Format:
    /ok/?url=<url>&user=<user>&groups=<group-list>&http_method=<http_method>&post_parameters=<post_parameters>

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
    - A 400 Error if the arguments were incorrectly provided
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
        return make_json_response("Expected a url argument", "400")
    if not (user or groups):
        return make_json_response("Expected a user or some groups", "400")
    if user:
        user = urldecode(user)
    if not USERS_DB.get(user):
        return make_json_response("User %s does not exist" % user, "404")
    if groups:
        try:
            groups = urldecode(groups).split(",")
        except TypeError:
            return make_json_response("Could not parse the groups", "400")
    else:
        groups = USERS_DB[user]["groups"]
    if post_parameters:
        try:
            post_parameters = urllib.parse_qs(post_parameters)
        except ValueError:
            return make_json_response("Could not parse post_parameters", "400")
    for group in groups:
        if not GROUPS_DB.get(group):
            return make_json_response("Group %s does not exist" % group,"404")

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
            return make_json_response("Could not parse http_query", "400")

    for group in groups:
        restrictions = GROUPS_DB[group]
        for path_pattern, restriction_list in restrictions.iteritems():
            if re.match(path_pattern, path):
                for restriction_name, restriction_params in restriction_list:
                    try:
                        rule = restrictions_manager.get(restriction_name)
                    except KeyError:
                        return make_json_response("%s: unknown restriction" %
                                restriction_name, "500")
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
                        return make_json_response("Not allowed", "403")
            return make_json_response(describe_user, "200")

    return make_json_response("Not allowed", "403")

@app.route("/users/")
@app.route("/users/<username>", methods=["GET", "POST", "DELETE"])
def users(username=None):
    """
    Documentation for users
    """
    if username is None:
        return flask.jsonify(USERS_DB)
    else:
        user = USERS_DB.get(username)
        if flask.request.method == "GET":
            if user is None:
                return make_json_response("Unknown user", "404")
            else:
                return flask.jsonify(user)
        if flask.request.method == "POST":
            try:
                groups = flask.request.form.get("groups", "users").split(",")
                groups = set(groups.split(","))
            except TypeError:
                return make_json_response("Could not parse groups", "400")
            for group in groups:
                if group not in GROUPS_DB:
                    GROUPS_DB [group] = {}
            groups.add("users")
            USERS_DB [username] = { "groups": list(groups) }
            return flask.jsonify({"message": "Content created or updated",
                "links": { "updated_user" : "/users/%s" % username }})
        if flask.request.method == "DELETE":
            if user is None:
                return make_json_response("Unknown user", "404")
            del USERS_DB[username]
            return make_json_response("/users/%s deleted" % username, "204")

@app.route("/groups/")
@app.route("/groups/<groupname>", methods=["GET", "POST", "DELETE"])
def groups(groupname=None):
    """
    Documentation for groups
    """
    if groupname is None:
        return flask.jsonify(GROUPS_DB)
    else:
        group = GROUPS_DB.get(groupname)
        if flask.request.method == "GET":
            if group is None:
                return make_json_response("Unknown group", "404")
            else:
                return flask.jsonify(group)
        if flask.request.method == "POST":
            try:
                posted_permissions = flask.request.form.get("conditions")
                if not posted_permissions:
                    conditions = {}
                else:
                    conditions = dict(
                            json.loads(urldecode(posted_permissions))
                            )
            except TypeError:
                return make_json_response(
                        "Could not parse provided conditions", "400"
                        )
            for condition in conditions:
                if condition not in condition_handler.all_conditions():
                    return make_json_response(
                            "condition %s does not exist" % condition,
                            "400"
                            )
            GROUPS_DB [groupname] = conditions
            return flask.jsonify({"message": "Content created or updated",
                "links": { "updated" : "/groups/%s" % groupname }})
        if flask.request.method == "DELETE":
            if group is None:
                return make_json_response("Unknown group", "404")
            del GROUPS_DB[groupname]
            for username, groups in USERS_DB.iteritems():
                if groupname in groups["groups"]:
                    groups["groups"].remove(groupname)
                    USERS_DB[username] = groups
            return make_json_response("/groups/%s deleted" % groupname, "204")

@app.route("/restrictions/")
@app.route("/restrictions/<restrictionname>")
def restrictions(restrictionname=None):
    if restrictionname is None:
        return flask.jsonify(restrictions_manager.all())
    else:
        description = restrictions_manager.all().get(restrictionname)
        if description is None:
            return make_json_response("Unknown restriction", "404")
        else:
            return flask.jsonify({ "description" : description })

@app.route("/")
@app.route("/app_info")
def app_info():
    res = dict()
    res["USERS_DB_PATH"] = USERS_DB_PATH
    res["GROUPS_DB_PATH"] = GROUPS_DB_PATH
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
        return make_json_response({"links": links})
    else:
        func = app.view_functions.get(endpoint, None)
    if not func:
        return make_json_response("%s: unkown endpoint" % str(endpoint), "404")
    if not func.__doc__:
        return make_json_response("%s: no documentation" % str(endpoint), "404")
    response = flask.make_response(func.__doc__)
    response.headers["Content-Type"] = "text/plain"
    return response
