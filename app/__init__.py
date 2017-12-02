#third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# db variable initialization
db = SQLAlchemy()

# login manager variable initialization
login_manager = LoginManager()

def create_app():
	app = Flask(__name__)
	app.config.from_object('config')
	db.init_app(app)
	login_manager.init_app(app)

	# Attempt to access registeres content will results in the following page redirect and message
	login_manager.login_message = "You must be logged in to access this page."
	login_manager.login_view = "auth.login"

	#migration variable initialiazation
	migrate = Migrate(app, db)

	from app import models

	#import each blueprint object and register it. For the admin blueprint, url prefix /admin was added
	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	return app