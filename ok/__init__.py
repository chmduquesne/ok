# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__, static_url_path="")

import ok.api
