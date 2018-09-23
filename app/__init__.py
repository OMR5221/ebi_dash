# app/__init__.py
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# Localm imports
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

# Create app based on input config file:
def create_app(config_name):
	app = FlaskAPI(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	# Deprectaed settiung that throws warning when not explicitly disabled:
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	
	return app