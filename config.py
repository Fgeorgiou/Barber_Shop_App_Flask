#Importing os module and defining application's path
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_ECHO = True

#Cross-site_request_forgery_(CSRF)_protection_provided_by_WTforms
WTF_CSRF_ENABLED = True

#The secret key that scrf uses for authentication
SECRET_KEY = 'This-must-be-changed'

#The path to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'barber_shop.db')

#By disabling this, we decrease the overload
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Reference: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing
# Mail Server Settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None