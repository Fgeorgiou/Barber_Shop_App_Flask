from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import ContactForm #, LoginForm, EditForm
# from .models import User
from datetime import datetime

#global variables
company_name = {'name' : 'LaKosta'} # Test
year = datetime.now().year

'''user_loader "callback" function. 
This callback is used to reload the user object from the user ID stored in the session.
It should take the Unicode ID of a user, and return the corresponding user object.'''
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title='Home',
                           company_name=company_name,
                           year=year)

@app.route('/about_us')
def about_us():
    return render_template("about_us.html",
                           title='About Us',
                           company_name=company_name,
                           year=year)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
      if form.validate() == False:
        flash('All fields are required.')
        return render_template('contact.html',
                           title='Contact',
                           company_name=company_name,
                           year=year,
                           form=form)
      else:
        return 'Form posted.'

    elif request.method == 'GET':
      return render_template("contact.html",
                           title='Contact',
                           company_name=company_name,
                           year=year,
                           form=form)

@app.route('/appointments')
def appointments():
    return render_template("appointments.html",
                           title='Appointments',
                           company_name=company_name,
                           year=year)

@app.route('/register')
def register():
    return render_template("register.html",
                           title='Register',
                           company_name=company_name,
                           year=year)

@app.route('/login')
def login():
    return render_template("login.html",
                           title='Login',
                           company_name=company_name,
                           year=year)

@app.route('/admin_interface')
def admin_interface():
    return render_template("admin_interface.html",
                           title='Admin_Interface',
                           company_name=company_name,
                           year=year)  