from flask import Flask, render_template, request, redirect, url_for, session, flash
import app.config
import os
from flask_orator import Orator
from app.libraries.util import Util as util

app = Flask(__name__, static_folder="statics")

env = os.environ.get('ALBASIA_ENV', 'development')
if env == 'production':
    app.config.from_object(config.ProductionConfig)
elif env == 'staging':
    app.config.from_object(config.StagingConfig)
elif env == 'development':
    app.config.from_object(config.DevelopmentConfig)

db = Orator(app)

if app.config['WEB_ENABLE']:
    from app.controllers.user import User
    User()
    from app.controllers.main import Main
    Main()