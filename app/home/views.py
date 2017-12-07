from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from .forms import ContactForm, UserAppointmentForm
from datetime import datetime, timedelta
from . import home
from ..models import *

#global variables
company_name = {'name' : 'LaKosta'} # Test
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


@home.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
  appointment_form = UserAppointmentForm()
  
  if request.method == 'POST':
    if appointment_form.validate_on_submit():
      '''
      !Criteria for an appointment to be valid!
      a. Cant make an appointment on any day before today
      b. Cant make an appointment on a time before now
      c. User cant have more than 1 active appointment to avoid intentional system overload
      '''
      #time variables neccesary for calculating appointment credibility
      today = datetime(year, month, day)
      time_string = appointment_form.appointment_time.data

      #Criteria a check
      if appointment_form.appointment_date.data < today.strftime('%m/%d/%Y'):
        flash ("Appointment can't be scheduled for a date before today" + today.strftime('%m/%d/%Y'), 'error')
      #Criteria b check
      elif appointment_form.appointment_date.data == today.strftime('%m/%d/%Y'):
        if time_string < datetime.now().time().strftime('%H:%M'):
          flash ("Appointment can't be scheduled for a time sooner than now! - Current Time: " + datetime.now().time().strftime('%H:%M'), 'error')
      else:
        #Time calculation function for appointment's end
        def nextTime(time, minutestoadd):
            base_time = datetime.strptime(time, "%H:%M")
            minutesobj = timedelta(minutes = minutestoadd)
            newtime = base_time + minutesobj
            return newtime.strftime('%H:%M')

        appointment = Appointment(appointment_date = appointment_form.appointment_date.data,
                                  appointment_start_time = appointment_form.appointment_time.data,
                                  appointment_end_time = nextTime(time_string, 30),
                                  customer_id = current_user.id,
                                  barber_id = appointment_form.barber.data,
                                  service_id = appointment_form.service.data,
                                  #appointment_cost = Service.query.get(service_id),
                                  made_by = current_user.id,
                                  timestamp = datetime.now())

        db.session.add(appointment)
        db.session.commit()
        flash('Appointment was scheduled successfully!', 'info')
            
        # redirect to the login page
        return redirect(url_for('home.my_account'))
    else:
      flash_errors(appointment_form)

  return render_template("home/appointments.html",
                           title='Appointments',
                           company_name=company_name,
                           year=year,
                           appointment_form=appointment_form)

@home.route('/my_account')
@login_required
def my_account():
    return render_template("home/my_account.html",
                           title='My Account',
                           company_name=company_name,
                           year=year)      