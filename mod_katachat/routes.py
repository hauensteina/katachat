
import json, re
from functools import wraps
import shortuuid
import requests

from flask import request, Response, send_file

from mod_katachat import app, log, REDIS, tojson
from mod_katachat.goboard import GoBoard,BLACK,WHITE

# API exception handling
#--------------------------
def api_error(f):
    """ A decorator to handle exceptions in API calls """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return {'exception':str(e)}, 500 
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

@app.route('/katachat/make_move/<string:game_id>/<string:move>', methods=['GET'])
@api_error
def make_move(game_id, move):
    """ Example: /katachat/make_move/1234/Be4 """
    data = REDIS.get(game_id) 
    if not data:
        return { 'error': 'game_id not found' }, 500
    data = json.loads(data)
    move = move.upper().strip()
    if not re.match(r'[BW][\s]*[a-i][1-9]', move, flags=re.IGNORECASE):
        return { 'error': f'move {move} not valid' }, 500
    moves = data['move_seq']
    prevcol = moves[-1][0] if moves else 'W'
    nextcol = 'B' if prevcol == 'W' else 'W'
    if move[0] != nextcol:
        return { 'error': f'move {move} has wrong color' }, 500
    moves.append(move)
    REDIS.set(game_id, tojson(data))
    resp = {'all_moves': moves}
    return resp

@app.route('/katachat/undo_last_move/<string:game_id>', methods=['GET'])
@api_error
def undo_last_move(game_id):
    """ Example: /katachat/undo_last_move/1234 """
    data = REDIS.get(game_id) 
    if not data:
        return { 'error': 'game_id not found' }, 500
    data = json.loads(data)
    moves = data['move_seq']
    moves.pop(-1)
    REDIS.set(game_id, tojson(data))
    resp = {'all_moves': moves}
    return resp

@app.route('/katachat/get_all_moves/<string:game_id>', methods=['GET'])
@api_error
def get_all_moves(game_id):
    """ Example: /katachat/get_all_moves/1234 """
    data = REDIS.get(game_id) 
    if not data:
        return { 'error': 'game_id not found' }, 500
    data = json.loads(data)
    moves = data['move_seq']
    resp = {'all_moves': moves}
    return resp

@app.route('/katachat/get_best_moves/<string:game_id>', methods=['GET'])
@api_error
def get_best_moves(game_id):
    data = REDIS.get(game_id) 
    if not data:
        return { 'error': 'game_id not found' }, 500
    data = json.loads(data)
    moves = data['move_seq']
    resp = fwd_to_katago_9(moves)
    best_moves = resp['diagnostics']['best_ten']
    return best_moves

@app.route('/katachat/get_score/<string:game_id>', methods=['GET'])
@api_error
def get_score(game_id):
    data = REDIS.get(game_id) 
    if not data:
        return { 'error': 'game_id not found' }, 500
    data = json.loads(data)
    moves = data['move_seq']
    resp = fwd_to_katago_9(moves)
    black_score = resp['diagnostics']['score']
    black_winprob = resp['diagnostics']['winprob']
    res = { 'black_score': black_score, 'black_winprob': black_winprob }
    return res

@app.route('/katachat/print_board/<string:game_id>', methods=['GET'])
@api_error
def print_board(game_id):
    data = REDIS.get(game_id) 
    if not data:
        return { 'error': 'game_id not found' }, 500
    data = json.loads(data)
    moves = data['move_seq']

    board = GoBoard(9)
    for move in moves: # 'BE4'
        color = move[0]
        move = move[1:]
        color = BLACK if color == 'B' else WHITE    
        board.play_move(move,color)
    diagram = str(board)
    return { 'diagram': diagram }

### Helpers
##################

def fwd_to_katago_9(moves):
    """ 
    Forward request to 9x9 katago server.
    Moves looks like [ 'Be4', 'W e6', 'bF5' ... ], case insensitive
    """
    moves = [ x.strip().upper() for x in moves ]
    moves = [ ( x[0], x[-2:] ) for x in moves ]
    colors = [ x[0] for x in moves ]
    moves = [ x[1] for x in moves ]

    args = {'board_size': 9, 'moves': moves, 'config':{'komi':6.5}}
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


### Utility funcs
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

