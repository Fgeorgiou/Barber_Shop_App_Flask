from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from .forms import ContactForm
from datetime import datetime
from . import home

#from app import app, db, login_manager

#global variables
company_name = {'name' : 'LaKosta'} # Test
year = datetime.now().year

@home.route('/')
@home.route('/index')
def index():
    return render_template("home/index.html",
                           title='Home',
                           company_name=company_name,
                           year=year)

@home.route('/about_us')
def about_us():
    return render_template("home/about_us.html",
                           title='About Us',
                           company_name=company_name,
                           year=year)

@home.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
      if form.validate() == False:
        flash('All fields are required.')
        return render_template('home/contact.html',
                           title='Contact',
                           company_name=company_name,
                           year=year,
                           form=form)
      else:
        return 'Form posted.'

    elif request.method == 'GET':
      return render_template("home/contact.html",
                           title='Contact',
                           company_name=company_name,
                           year=year,
                           form=form)


@home.route('/appointments')
@login_required
def appointments():
    return render_template("home/appointments.html",
                           title='Appointments',
                           company_name=company_name,
                           year=year)

@home.route('/my_account')
@login_required
def my_account():
    return render_template("home/my_account.html",
                           title='My Account',
                           company_name=company_name,
                           year=year)      