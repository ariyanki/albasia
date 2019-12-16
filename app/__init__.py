import app.config
import orator
import os
import logging.handlers
import redis
import pprint, sys
import traceback
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, json
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_claims
from flask_orator import Orator
from app.libraries.util import Util as util
from werkzeug.contrib.cache import RedisCache
from app.libraries.exceptions import InvalidResponseException, GeneralResponseException, ConnectionTimeoutException
from logstash_formatter import LogstashFormatterV1

app = Flask(__name__, static_folder="static")

env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(config.ProductionConfig)
elif env == 'staging':
    app.config.from_object(config.StagingConfig)
elif env == 'development':
    app.config.from_object(config.DevelopmentConfig)

api = Api(app)
db = Orator(app)
jwt = JWTManager(app)
revoked_store = redis.StrictRedis(
    host=app.config['CACHE_REDIS_HOST'],
    port=app.config['CACHE_REDIS_PORT'],
    db=0,
    decode_responses=True)
cache = RedisCache(
    host=app.config['CACHE_REDIS_HOST'],
    port=app.config['CACHE_REDIS_PORT'],
    default_timeout=app.config['CACHE_DEFAULT_TIMEOUT'],
    key_prefix=app.config['CACHE_KEY_PREFIX'])

#load routes
from app.routes import Route
Route()

 # Enable query log for development
env = os.environ.get('FLASK_ENV', 'development')
if env == 'development' and app.config['LOG_QUERY']:
    logger = logging.getLogger('orator.connection.queries')
    logger.setLevel(logging.DEBUG)
    logging.warning('Orator query log started')

# Log
handlers = [
    logging.handlers.RotatingFileHandler(
        "%s/%s" % (
            app.root_path,
            app.config['LOG_RESOURCE_PATH']),
        encoding= app.config['BLUEPRINT']['LOGS']['FILE_ENCODING'],
        maxBytes= int(app.config['BLUEPRINT']['LOGS']['FILE_MAX_BYTES']),
        backupCount= int(app.config['BLUEPRINT']['LOGS']['FILE_BACKUP_COUNT'])),
    logging.StreamHandler()
]
fmt = {
    'extra': {
        'type': 'albasia-local'
    }
}
jfmt = json.dumps(fmt)
logsts_formatter = LogstashFormatterV1(
    fmt=jfmt,
    datefmt="%Y-%m-%d %H:%M:%S")
app.logger.setLevel(logging.DEBUG)
for h in handlers:
    h.setFormatter(logsts_formatter)
    app.logger.addHandler(h)

# Exception Handler
# Invalid response
@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'

@app.errorhandler(ConnectionTimeoutException)
def handle_exception(error):
    data = error.get_body()

    logRequest(data, error.get_code())

    return jsonify(data), error.get_code()

@app.errorhandler(GeneralResponseException)
def handle_exception(error):
    data = error.get_body()

    logRequest(data, error.get_code())

    return jsonify(data), error.get_code()

@app.errorhandler(InvalidResponseException)
def handle_exception(error):
    data = error.get_body()

    logRequest(data, error.get_code())

    return jsonify(data), error.get_code()

# Exception response
@app.errorhandler(Exception)
def handle_exception(error):
    pprint.pprint(error)
    exc_type, exc_obj, tb = sys.exc_info()
    message = [str(x) for x in error.args]
    # status_code = 500

    if any("blacklist.py" in s for s in traceback.format_tb(tb)):
        data = {
            'message': {
                'title': 'Token Expired',
                'body': 'Token has expired.'
            }
        }

        logRequest(data, VariableConstant.TOKEN_EXPIRED_STATUS_CODE)

        return jsonify(data), VariableConstant.TOKEN_EXPIRED_STATUS_CODE

    # need to be fixed (response code)
    status_code= 500
    data = {
        'message': {
            'title': 'Error',
            'body': 'Internal Server Error'
        },
        'data': {
            'type': error.__class__.__name__,
            'traces': traceback.format_tb(tb)
        }
    }

    logRequest(data, status_code)

    traceback.print_exc()
    return jsonify(data), status_code


@app.errorhandler(orator.exceptions.query.QueryException)
def handle_query_exception(error):

    message = str(error.args[2])

    if type(message) == list:
        error_message= message
    else:
        error_message=[message]

    data = {
        'message': {
            'title': "Query Error",
            'body': "Please check your error"
        },
        'data':{
            'errors':error_message
        }
    }

    logRequest(data, 422)

    return jsonify(data), 422

def logRequest(data, status_code):
    if (request.method == "GET") or (request.method == "DELETE"):
        request_data = ''
    else:
        request_data = request.get_json()

    claims = get_jwt_claims()
    
    error_data = {
        'endpoint': request.method + " " + request.path,
        'status_code': status_code,
        'user_claim': claims,
        'request': request_data,
        'response': data
    }
    app.logger.error('ERROR API RESPONSE',error_data)
