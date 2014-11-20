#!env python2
from urlparse import urlparse
from flask import Flask, request, jsonify
from xdg.BaseDirectory import save_config_path, save_data_path
from kyotocabinetdict import KyotoCabinetDict
import os
import sys
import json

app = Flask(__name__)

# load the user configured functions
APP_NAME = "ok"
CONFIG_DIR = save_config_path(APP_NAME)
DB_PATH = os.path.join(save_data_path(APP_NAME), "users.kch")
sys.path.append(CONFIG_DIR)
try:
    import config
except ImportError:
    pass

DB = KyotoCabinetDict(DB_PATH)
#DB = dict()

@app.route("/")
def ok():
    res = dict(request.args)
    url = None
    user = None
    method = "GET"
    res["data_home"] = save_data_path("ok")
    res["config_home"] = save_config_path("ok")
    return jsonify(res)

@app.route("/add_user/<username>")
def add_user(username):
    if DB.get(username, None):
        return "The %s already exists!" % username
    DB [username] = json.dumps({"groups": []})
    return "Added user %s" % username

@app.route("/add_group/<groupname>")
def add_group(groupname):
    return "Added group %s" % groupname

@app.route("/set_groups/<username>/<grouplist>")
def set_groups():
    pass

def get_groups(user):
    return [ "users" ]

if __name__ == "__main__":
    app.run()
