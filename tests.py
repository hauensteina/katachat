#!/usr/bin/env python

# /********************************************************************
# Filename: katachat/main.py
# Author: AHN
# Creation Date: May 2023
# **********************************************************************/
#
# Main entry point for the katachat ChatGPT plugin

from pprint import pprint
import yaml
from mod_katachat import routes
from openapi_parser import parse

def main():
    # Try to parse the openapi.yaml file
    try:
        content = parse('openapi.yaml')
    except Exception as exc:
        print(exc)

    # Testing Katago server
    resp = routes.fwd_to_katago_9(['Be4', 'W e6', 'bF5'])
    print('Request:')
    print("routes.fwd_to_katago_9(['Be4', 'W e6', 'bF5'])")
    print('Response:')
    pprint(resp)
    best_move = resp['diagnostics']['best_ten'][0]['move']
    pprint(f'{best_move=}')

    # Testing routes
    game_id = routes.start_game()['game_id']
    print(f'{game_id=}')

    print('Request:')
    print("routes.make_move(game_id, 'Be4')")
    resp = routes.make_move(game_id, 'Be4')
    print(f'{resp=}')

    print('Request:')
    print("routes.make_move(game_id, 'We6')")
    resp = routes.make_move(game_id, 'We6')
    print(f'{resp=}')

    print('Request:')
    print("routes.get_best_moves(game_id)")
    resp = routes.get_best_moves(game_id)
    print(f'{resp=}')

    print('Request:')
    print("routes.print_board(game_id)")
    resp = routes.print_board(game_id)
    print(resp['diagram'])

    print('Request:')
    print("routes.get_all_moves(game_id)")
    resp = routes.get_all_moves(game_id)
    print(f'{resp=}')

    print('Request:')
    print("routes.get_score(game_id)")
    resp = routes.get_score(game_id)
    print(f'{resp=}')

    print('Request:')
    print("routes.undo_last_move(game_id)")
    resp = routes.undo_last_move(game_id)
    print(f'{resp=}')

    print('Request:')
    print("routes.get_all_moves(game_id)")
    resp = routes.get_all_moves(game_id)
    print(f'{resp=}')

main()


"""
Lets play a game of Go!
"""