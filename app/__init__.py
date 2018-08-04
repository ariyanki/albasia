from flask import Flask
import app.config
import os

app = Flask(__name__, static_folder="static")

@app.route("/")
def hello():
	return "Hai World!"

env = os.environ.get('ALBASIA_ENV', 'development')
if env == 'production':
	app.config.from_object(config.ProductionConfig)
elif env == 'staging':
    app.config.from_object(config.StagingConfig)
elif env == 'development':
    app.config.from_object(config.DevelopmentConfig)
