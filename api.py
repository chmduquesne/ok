#!env python2
from urlparse import urlparse
import urllib2
import flask
from flask import Flask, request, jsonify, abort
from xdg.BaseDirectory import save_config_path, save_data_path
from kyotocabinetdict import KyotoCabinetDict
import permissions
from permissionhandler import permission_handler
import os
import sys
import json

app = Flask(__name__)

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

@app.route("/")
def ok():
    arg_method = request.args.get("method", "GET")
    arg_groups = request.args.get("groups")
    arg_user = request.args.get("user")
    arg_url = request.args.get("url")

    if not arg_user or not arg_url:
        response = jsonify({"Message": "missing user/url"})
        response.status = "400"
        return response

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

    response = jsonify({"Message": "User is not allowed to performed the request"})
    response.status = "403"
    return response



def add_user(username):
    user = USERS_DB.get(username)
    if user:
        return "The user %s already exists!" % username
    USERS_DB [username] = { "groups": [ "users", username] }
    return "Added user %s" % username

def get_groups(username):
    groups = USERS_DB.get(username)
    if groups is None:
        flask.abort(404)
    return jsonify(groups)

@app.route("/users")
def list_users():
    return flask.jsonify({"users": USERS_DB.keys()})

@app.route("/users/<username>", methods=['GET', 'POST'])
def users(username):
    if request.method == 'GET':
        return get_groups(username)
    if request.method == 'POST':
        return add_user(username, request.form.get("groups", None))

@app.route("/add_group/<groupname>")
def add_group(groupname):
    group = GROUPS_DB.get(groupname)
    if group:
        return "The group %s already exists!" % username
    GROUPS_DB [group] = { "permissions": [] }
    return "Added group %s" % groupname

@app.route("/set_permissions/<groupname>")
def set_permissions(groupname):
    group = GROUPS_DB.get(groupname)
    if group:
        return "The group %s already exists!" % username
    GROUPS_DB [group] = { "permissions": [] }
    return "Added group %s" % groupname

@app.route("/set_groups/<username>/<grouplist>")
def set_groups(username, grouplist):
    pass

@app.route("/permissions")
@app.route("/permissions/<groupname>", methods=['GET', 'POST'])
def get_permissions(group=None):
    if group is None:
        return jsonify(permission_handler.list_permissions())
    else:
        if request.method == 'GET':
            return jsonify(GROUPS_DB[group])

@app.route("/app_info")
def app_info():
    res = dict()
    res["USERS_DB_PATH"] = USERS_DB_PATH
    res["GROUPS_DB_PATH"] = GROUPS_DB_PATH
    res["CONFIG_FILE"] = os.path.join(CONFIG_DIR, "config.py")
    return jsonify(res)

if __name__ == "__main__":
    app.run()
