# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
import os
HTTP_Server_App = Flask(__name__, static_folder='img')
HTTP_Server_App.config['JSON_AS_ASCII'] = False

HTTP_Server_App_PIPE_R, HTTP_Server_App_PIPE_W = os.pipe()


@HTTP_Server_App.route('/')
def index():
    return 'welcome to huayajun\'s flask web server'


@HTTP_Server_App.route("/get",  methods=['GET', 'POST'])
def http_get_info():
    try:
        w = os.fdopen(HTTP_Server_App_PIPE_W, 'w')
        w.write(request.form)
    except Exception, e:
        print e


@HTTP_Server_App.route("/set", methods=['POST', 'POST'])
def http_set_action():
    try:
        w = os.fdopen(HTTP_Server_App_PIPE_W, "w")
        w.write(request.form)
    except Exception, e:
        print e


@HTTP_Server_App.errorhandler(404)
def page_not_found(error):
   page = u"""
        <html>
        <head>
            <title>404你懂的 </title>
        </head>
        <body>
        <h3>404,你还不懂么？</h3>
        </body>
        </html>
    """
   return page