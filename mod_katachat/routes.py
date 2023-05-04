from pdb import set_trace as BP

import os, sys, json
from datetime import date
import shortuuid
import shutil

import flask
from flask import request, Response, jsonify, send_file

from mod_katachat import app, log

#app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
_TODOS = {}

#@app.post("/todos/<string:username>")
@app.route('/todos/<string:username>', methods=['POST'])
def add_todo(username):
    parms = get_parms()
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(parms["todo"])
    return 'OK'

#@app.get("/todos/<string:username>")
@app.route('/todos/<string:username>', methods=['GET'])
def get_todos(username):
    res = _TODOS.get(username, [])
    return jsonify(res)

#@app.delete("/todos/<string:username>")
@app.route('/todos/<string:username>', methods=['DELETE'])
def delete_todo(username):
    parms = get_parms()
    todo_idx = parms["todo_idx"]
    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return 'OK'

#@app.get("/logo.png")
@app.route("/logo.png", methods=['GET'])
def plugin_logo():
    filename = '../logo.png'
    return send_file(filename)

#@app.get("/.well-known/ai-plugin.json")
@app.route("/.well-known/ai-plugin.json", methods=['GET'])
def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return Response(text, mimetype="text/json")

#@app.get("/openapi.yaml")
@app.route("/openapi.yaml")
def openapi_spec():
    #host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return Response(text, mimetype="text/yaml")

# Utility funcs
##################

#------------------
def get_parms():
    if request.method == 'POST': # Form submit
        parms = dict(request.form)
    else:
        parms = dict(request.args)
    # strip all parameters    
    parms = { k:v.strip() for k, v in parms.items()}
    print(f'>>>>>>>>>PARMS:{parms}')
    return parms
