# /********************************************************************
# Filename: mod_katachat/__init__.py
# Author: AHN
# Creation Date: May, 2023
# **********************************************************************/
#
# Imports, Constants, DB-connections... 
#

from pdb import set_trace as BP

import os
import datetime
from urllib.parse import urlparse
import redis
from flask import Flask
from flask_cors import CORS
import json

app = Flask( __name__)
#app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app, resources={r"/katachat/*": {"origins": "*"}}, headers='Content-Type')
CORS(app)

# Our own exception class
#----------------------------
class AppError(Exception):
    pass

#---------------------------
def log( msg, level=''):
    """ Logging. Change as needed """
    print(msg, flush=True)

# Make sure dates are serialized as yyyy-mm-dd by flask.jsonify (for our API endpoints)
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return json.JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

def tojson(obj):
    """ Convenience func to use our custom encoder """
    return json.dumps(obj, cls=CustomJSONEncoder)

app.config.update(
    DEBUG = True,
    SECRET_KEY = os.environ['AHX_FLASK_SECRET'] # For encrypted session cookie
)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 

if os.getenv('PRODUCTION_FLAG'):
    redis_url = os.getenv('REDIS_TLS_URL')
else:
    redis_url = os.getenv('REDIS_URL')  # local

log('>>>>>>>>> REDIS_URL:' + redis_url)

url = urlparse(redis_url)
ssl=True
if url.hostname == 'localhost': ssl=False
REDIS = redis.Redis(host=url.hostname, port=url.port,
                    username=url.username, password=url.password,
                    ssl=ssl, ssl_cert_reqs=None)

# Endpoints
#---------------------
from mod_katachat import routes

