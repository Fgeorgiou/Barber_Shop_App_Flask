from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import basedir
from flask_login import LoginManager
from flask_migrate import Migrate

# db variable initialization
db = SQLAlchemy()

# login manager variable initialization
login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
login_manager.init_app(app)

# Attempt to access registeres content will results in the following page redirect and message
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

#migration variable initialiazation
migrate = Migrate(app, db)

# this import statement is at the end of the script to avoid circular references
from app import views, models