from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from .forms import ContactForm
from datetime import datetime, timedelta
from sqlalchemy import and_
from . import home
from ..models import *

#global variables
company_name = {'name' : 'LaBarberia'}
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')

@home.route('/')
@home.route('/index')
def index():

  #Query for collecting the services
  services_list = db.session.query(Service).order_by(Service.name)

  return render_template("home/index.html",
                         title='Home',
                         company_name=company_name,
                         year=year,
                         services_list=services_list)

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
        flash('All fields are required.', 'error')
        return render_template('home/contact.html',
                           title='Contact',
                           company_name=company_name,
                           year=year,
                           form=form)
      else:
        flash('Mail Sent. Thanks for your time!', 'info')
        return render_template('home/contact.html',
                   title='Contact',
                   company_name=company_name,
                   year=year,
                   form=form)
    elif request.method == 'GET':
      return render_template("home/contact.html",
                           title='Contact',
                           company_name=company_name,
                           year=year,
                           form=form)
  