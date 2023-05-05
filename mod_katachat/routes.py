from pdb import set_trace as BP

import os, sys, json
from datetime import date
from functools import wraps
import shortuuid
import shutil
import requests

import flask
from flask import request, Response, jsonify, send_file
from flask_cors import cross_origin

from mod_katachat import app, log, REDIS, tojson

# API exception handling
#--------------------------
def api_error(f):
    """ A decorator to handle exceptions in API calls """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return {'error':str(e)}, 500 
    return decorated

### Endpoints
##################

@app.route('/katachat/start_game', methods=['GET'])
@api_error
def start_game():
    game_id = shortuuid.uuid()
    data =  {'game_id': game_id, 'move_seq': []}
    REDIS.set(game_id, tojson(data))
    return { 'game_id': game_id }

@app.route('/katachat/get_best_move/<string:game_id>', methods=['GET'])
@api_error
def get_best_move(game_id):
    data = REDIS.get(game_id) 
    if not data:
        return { 'error': 'game_id not found' }, 500
    data = json.loads(data)
    moves = data['move_seq']
    res = fwd_to_katago_9(moves)
    log(res)
    return res

# Helpers
##################

def fwd_to_katago_9(moves):
    """ 
    Forward request to 9x9 katago server.
    """
    moves = [ m[1] for m in moves ] # we don't need the color
    args = {'board_size': 9, 'moves': moves}
    URL = 'https://katagui.baduk.club/select-move-9/katago_gtp_bot'
    resp = requests.post(URL, json=args)
    try:
        res = resp.json()
    except Exception as e:
        print('Exception in fwd_to_katago_9()')
        print(f'moves: {moves}')
    return res 

@app.route("/logo.png", methods=['GET'])
def plugin_logo():
    filename = '../logo.png'
    return send_file(filename)

@app.route("/.well-known/ai-plugin.json", methods=['GET'])
def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return Response(text, mimetype="text/json")

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
