#!env python2
from urlparse import urlparse
import urllib2
import flask
from flask import Flask, request, jsonify
from xdg.BaseDirectory import save_config_path, save_data_path
from kyotocabinetdict import KyotoCabinetDict
import conditions
from conditionhandler import condition_handler
import os
import sys
import json
import traceback

from ok import app

# load the user configured functions
APP_NAME = "ok"
CONFIG_DIR = save_config_path(APP_NAME)
USERS_DB_PATH = os.path.join(save_data_path(APP_NAME), "users.kch")
GROUPS_DB_PATH = os.path.join(save_data_path(APP_NAME), "groups.kch")
PERMISSIONS_DB_PATH = os.path.join(save_data_path(APP_NAME), "permissions.kch")
sys.path.append(CONFIG_DIR)
try:
    import config
except ImportError:
    pass

USERS_DB = KyotoCabinetDict(USERS_DB_PATH)
GROUPS_DB = KyotoCabinetDict(GROUPS_DB_PATH)
PERMISSIONS_DB = KyotoCabinetDict(PERMISSIONS_DB_PATH)

def urlencode(s):
    return urllib2.quote(s)

def urldecode(s):
    return urllib2.unquote(s).decode('utf-8')

def make_json_response(message, status="200"):
    response = jsonify({"message": message})
    response.status = status
    return response

def evaluate(permission, request):
    return True

@app.route("/ok/")
def ok():
    """
    Expected format /ok/?url=<url>&user=tom&groups=g1,g2&method=GET
    """

    url = request.args.get("url", None)
    groups = request.args.get("groups", None)
    user = request.args.get("user", None)
    method = urldecode(request.args.get("method", "GET"))

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

    for group in groups:
        if not GROUPS_DB.get(group):
            return make_json_response("Group %s does not exist" % group,"404")

    url_parts = urlparse(url)
    scheme = url_parts.scheme
    netloc = url_parts.netloc
    path = url_parts.path
    query_params = url_parts.params
    query = url_parts.query
    hostname = url_parts.hostname
    port = url_parts.port

    # A request is allowed if any of the groups has a condition that
    # allows it.
    # A condition allows a request if all the conditions of this
    # condition return true.
    for group in groups:
        allowed = False
        conditions = GROUPS_DB[group]
        for condition, conditions_param in conditions:
            permission_checker = condition_handler.get(condition)
            if not condition_handler.get(condition)(scheme=scheme,
                        netloc=netloc, path=path, query_params=query_params,
                        query=query, hostname=hostname, port=port,
                        conditions_param=conditions_param):
                break

    return make_json_response("Not allowed", "403")

@app.route("/users/")
@app.route("/users/<username>", methods=["GET", "POST", "DELETE"])
def users(username=None):
    """
    Documentation for users
    """
    if username is None:
        return jsonify(USERS_DB)
    else:
        user = USERS_DB.get(username)
        if request.method == "GET":
            if user is None:
                return make_json_response("Unknown user", "404")
            else:
                return jsonify(user)
        if request.method == "POST":
            try:
                groups = request.form.get("groups", "users").split(",")
                groups = set(groups.split(","))
            except TypeError:
                return make_json_response("Could not parse groups", "400")
            for group in groups:
                if group not in GROUPS_DB:
                    GROUPS_DB [group] = {}
            groups.add("users")
            USERS_DB [username] = { "groups": list(groups) }
            return jsonify({"message": "Content created or updated",
                "links": { "updated_user" : "/users/%s" % username }})
        if request.method == "DELETE":
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
        return jsonify(GROUPS_DB)
    else:
        group = GROUPS_DB.get(groupname)
        if request.method == "GET":
            if group is None:
                return make_json_response("Unknown group", "404")
            else:
                return jsonify(group)
        if request.method == "POST":
            try:
                posted_permissions = request.form.get("conditions")
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
            return jsonify({"message": "Content created or updated",
                "links": { "updated" : "/groups/%s" % groupname }})
        if request.method == "DELETE":
            if group is None:
                return make_json_response("Unknown group", "404")
            del GROUPS_DB[groupname]
            for username, groups in USERS_DB.iteritems():
                if groupname in groups["groups"]:
                    groups["groups"].remove(groupname)
                    USERS_DB[username] = groups
            return make_json_response("/groups/%s deleted" % groupname, "204")

@app.route("/permissions/")
@app.route("/permissions/<permissionname>", methods=["GET", "POST", "DELETE"])
def permission(permissionname=None):
    if permissionname == None:
        return jsonify(PERMISSIONS_DB)
    else:
        permission = PERMISSIONS_DB.get(permissionname)

@app.route("/conditions/")
@app.route("/conditions/<conditionname>")
def conditions(conditionname=None):
    if conditionname is None:
        return jsonify(condition_handler.all_conditions())
    else:
        condition = condition_handler.all_conditions().get(conditionname)
        if condition is None:
            return make_json_response("Unknown condition", "404")
        else:
            return jsonify({ "description" : condition })

@app.route("/")
@app.route("/app_info")
def app_info():
    res = dict()
    res["USERS_DB_PATH"] = USERS_DB_PATH
    res["GROUPS_DB_PATH"] = GROUPS_DB_PATH
    res["PERMISSIONS_DB_PATH"] = PERMISSIONS_DB_PATH
    res["CONFIG_FILE"] = os.path.join(CONFIG_DIR, "config.py")
    res["links"] = "/help/"
    return jsonify(res)

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
    return func.__doc__
