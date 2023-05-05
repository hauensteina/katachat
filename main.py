#!/usr/bin/env python

# /********************************************************************
# Filename: katachat/main.py
# Author: AHN
# Creation Date: May 2023
# **********************************************************************/
#
# Main entry point for the katachat ChatGPT plugin

from pdb import set_trace as BP
from mod_katachat import app

#----------------------------
if __name__ == '__main__':    app.run( host='0.0.0.0', port=5003, debug=True)
    # If you want to run with gunicorn:
    # $ gunicorn app:app -w 1 -b 0.0.0.0:8000 --reload --timeout 1000
