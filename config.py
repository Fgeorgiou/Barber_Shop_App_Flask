#Importing os module and defining application's path
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Debug option. Disable in production
DEBUG = True

#Cross-site_request_forgery_(CSRF)_protection_provided_by_WTforms
WTF_CSRF_ENABLED = True

#The secret key that scrf uses for authentication
SECRET_KEY = 'This-must-be-changed'

#The path to our database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'barber-shop.db')

#Disabling this, decreases the overload
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Reference: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing
# Mail Server Settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Administrator List
ADMINS = ['you@example.com']