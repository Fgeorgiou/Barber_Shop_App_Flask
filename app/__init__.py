from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'index'
db = SQLAlchemy(app)

# this import statement is at the end of the script to avoid circular references
from app import views, models