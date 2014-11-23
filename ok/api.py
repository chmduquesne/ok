#!env python2
from urlparse import urlparse
import urllib2
import flask
from flask import Flask, request, jsonify
from xdg.BaseDirectory import save_config_path, save_data_path
from kyotocabinetdict import KyotoCabinetDict
import permissions
from permissionhandler import permission_handler
import os
import sys
import json

from ok import app

# load the user configured functions
APP_NAME = "ok"
CONFIG_DIR = save_config_path(APP_NAME)
USERS_DB_PATH = os.path.join(save_data_path(APP_NAME), "users.kch")
GROUPS_DB_PATH = os.path.join(save_data_path(APP_NAME), "groups.kch")
sys.path.append(CONFIG_DIR)
try:
    import config
except ImportError:
    pass

USERS_DB = KyotoCabinetDict(USERS_DB_PATH)
GROUPS_DB = KyotoCabinetDict(GROUPS_DB_PATH)

def urlencode(s):
    return urllib2.quote(s)

def urldecode(s):
    return urllib2.unquote(s).decode('utf-8')

def make_json_response(message, status="200"):
    response = jsonify({"message": message})
    response.status = status
    return response

@app.route("/")
def ok():
    arg_method = request.args.get("method", "GET")
    arg_groups = request.args.get("groups")
    arg_user = request.args.get("user")
    arg_url = request.args.get("url")

    if not arg_user or not arg_url:
        return make_json_response("missing user or url", "400")

    method = urldecode(arg_method)
    user = urldecode(arg_user)
    url = urldecode(arg_url)
    url_parts = urlparse(url)

    scheme = url_parts.scheme
    netloc = url_parts.netloc
    path = url_parts.path
    query_params = url_parts.params
    query = url_parts.query
    hostname = url_parts.hostname
    port = url_parts.port

    if arg_groups:
        groups = json.loads(urldecode(arg_groups))
    else:
        groups = get_groups(user)

    for group in groups:
        permissions = get_permissions(group)
        for permission, permission_params in permissions:
            if permission_handler.get(permission)(scheme=scheme,
                        netloc=netloc, path=path, query_params=query_params,
                        query=query, hostname=hostname, port=port,
                        permission_params=permission_params):
                return jsonify({})

    return make_json_response("Not allowed", "403")

@app.route("/users")
@app.route("/users/<username>", methods=["GET", "POST", "DELETE"])
def users(username=None):
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
                groups = set(json.loads(request.form.get("groups", '["users"]')))
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

@app.route("/groups")
@app.route("/groups/<groupname>", methods=["GET", "POST", "DELETE"])
def groups(groupname=None):
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
                permissions = dict(json.loads(request.form.get("permission", '{}')))
            except TypeError:
                return make_json_response("Could not parse provided permissions", "400")
            for permission in permissions:
                if permission not in permission_handler.list_permissions():
                    return make_json_response("Permission %s does not exist" % permission, "400")
            GROUPS_DB [groupname] = permissions
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

@app.route("/permissions")
@app.route("/permissions/<permissionname>")
def permissions(permissionname=None):
    if permissionname is None:
        return jsonify(permission_handler.list_permissions())
    else:
        permission = permission_handler.list_permissions().get(permissionname)
        if permission is None:
            return make_json_response("Unknown permission", "404")
        else:
            return jsonify({ "description" : permission })

@app.route("/app_info")
def app_info():
    res = dict()
    res["USERS_DB_PATH"] = USERS_DB_PATH
    res["GROUPS_DB_PATH"] = GROUPS_DB_PATH
    res["CONFIG_FILE"] = os.path.join(CONFIG_DIR, "config.py")
    return jsonify(res)

if __name__ == "__main__":
    app.run()
