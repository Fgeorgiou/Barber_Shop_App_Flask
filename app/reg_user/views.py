from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from .forms import UserAppointmentForm, EditEmailForm, EditFirstNameForm, EditLastNameForm, EditPasswordForm, EditTelephoneForm
from datetime import datetime, timedelta
from sqlalchemy import and_
from . import reg_user
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

@reg_user.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
  appointment_form = UserAppointmentForm()

  #Setting today's info
  today = datetime(year, month, day)
  #Querying for a current appointment
  current_appointment = db.session.query(Appointment).filter(and_(Appointment.appointment_date >= today.strftime('%m/%d/%Y'),
                                      Appointment.appointment_start_time > datetime.now().time().strftime('%H:%M'),
                                      Appointment.customer_id == current_user.id,
                                      Appointment.attendance == "Pending")).first()
  
  #Querying for any pending appointments with the selected barber and time of the user
  existing_appointment = db.session.query(Appointment).filter(and_(Appointment.appointment_date == appointment_form.appointment_date.data,
                                      Appointment.appointment_start_time == appointment_form.appointment_time.data,
                                      Appointment.barber_id == appointment_form.barber.data,
                                      Appointment.attendance == "Pending")).first()

  if request.method == 'POST':
    if appointment_form.validate_on_submit():
      '''
      !Criteria for an appointment to be valid!
      a. Cant make an appointment on any day before today
      b. Cant make an appointment on a time before now
      c. User cant have more than 1 active appointment to avoid intentional system overload
      d. An appointment cant be scheduled on a time that is already taken. A suggestion of another time or barber will be made
      '''
      #time variables neccesary for calculating appointment credibility
      today = datetime(year, month, day)
      time_string = appointment_form.appointment_time.data

      #Criteria a check
      if appointment_form.appointment_date.data < today.strftime('%m/%d/%Y'):
        flash ("Appointment can't be scheduled for a date before today" + today.strftime('%m/%d/%Y'), 'error')
      #Criteria b check
      elif appointment_form.appointment_date.data == today.strftime('%m/%d/%Y') and time_string < datetime.now().time().strftime('%H:%M'):
        flash ("Appointment can't be scheduled for a time sooner than now! - Current Time: " + datetime.now().time().strftime('%H:%M'), 'error')
      elif current_appointment is not None:
        flash ("You already have an active appointment. Please cancel it or contact the shop to schedule another.", 'error')
      elif existing_appointment is not None:
        flash ("There is another appointment at that time. Sorry for the inconvenience, try picking another time or barber.", 'error')
      else:
        #Time calculation function for appointment's end
        def nextTime(time, minutestoadd):
            base_time = datetime.strptime(time, "%H:%M")
            minutesobj = timedelta(minutes = minutestoadd)
            newtime = base_time + minutesobj
            return newtime.strftime('%H:%M')

        #calculate the appointment cost based on the user's selection
        service_to_evaluate = Service.query.filter_by(id=appointment_form.service.data).first()
        service_discount = int(service_to_evaluate.cost) - (int(service_to_evaluate.cost) / 10)
        service_cost = str(service_discount)

        #Database query for appointment
        appointment = Appointment(appointment_date = appointment_form.appointment_date.data,
                                  appointment_start_time = appointment_form.appointment_time.data,
                                  appointment_end_time = nextTime(time_string, 30),
                                  appointment_cost = service_cost,
                                  customer_id = current_user.id,
                                  barber_id = appointment_form.barber.data,
                                  service_id = appointment_form.service.data,
                                  made_by = current_user.id,
                                  timestamp = datetime.now())

        db.session.add(appointment)
        db.session.commit()
        flash('Appointment was scheduled successfully!', 'info')
            
        # redirect to the login page
        return redirect(url_for('reg_user.my_account'))
    else:
      flash_errors(appointment_form)

  return render_template("reg_user/appointments.html",
                           title='Appointments',
                           company_name=company_name,
                           year=year,
                           appointment_form=appointment_form,
                           current_appointment=current_appointment)

@reg_user.route('/my_account')
@login_required
def my_account():

  #Setting today's info
  today = datetime(year, month, day)
  #Querying for a current appointment
  current_appointment = db.session.query(Appointment).filter(and_(Appointment.appointment_date >= today.strftime('%m/%d/%Y'),
                                        Appointment.appointment_start_time > datetime.now().time().strftime('%H:%M'),
                                        Appointment.customer_id == current_user.id,
                                        Appointment.attendance == "Pending")).first()

  #Querying for the appointment history of the user
  appointment_history = Appointment.query.filter(Appointment.customer_id == current_user.id).order_by(Appointment.appointment_date.desc(), Appointment.appointment_start_time.desc())

  return render_template("reg_user/my_account.html",
                         title='My Account',
                         company_name=company_name,
                         year=year,
                         current_appointment=current_appointment,
                         appointment_history=appointment_history)    

@reg_user.route('/edit_email', methods=['GET', 'POST'])
@login_required
def edit_email():

  current_edit = User.query.filter_by(id = current_user.id).first()
  edit_email_form = EditEmailForm()

  if request.method == 'POST':
    if edit_email_form.validate_on_submit:
      current_edit.email = edit_email_form.email.data
      db.session.commit()
      flash('Successfully Edited e-mail!')

      return redirect(url_for('reg_user.my_account'))
    else:
      flash('Something went wrong!','error')

  return render_template("reg_user/edit_personal_info/edit_email.html",
                     title='My Account',
                     company_name=company_name,
                     year=year,
                     current_edit=current_edit,
                     edit_email_form=edit_email_form)    

@reg_user.route('/edit_first_name', methods=['GET', 'POST'])
@login_required
def edit_first_name():

  current_edit = User.query.filter_by(id = current_user.id).first()
  edit_first_name_form = EditFirstNameForm()

  if request.method == 'POST':
    if edit_first_name_form.validate_on_submit:
      current_edit.first_name = edit_first_name_form.first_name.data
      db.session.commit()
      flash('Successfully edited First name!')

      return redirect(url_for('reg_user.my_account'))
    else:
      flash_errors(edit_first_name_form)

  return render_template("reg_user/edit_personal_info/edit_first_name.html",
                     title='My Account',
                     company_name=company_name,
                     year=year,
                     current_edit=current_edit,
                     edit_first_name_form=edit_first_name_form)  

@reg_user.route('/edit_last_name', methods=['GET', 'POST'])
@login_required
def edit_last_name():

  current_edit = User.query.filter_by(id = current_user.id).first()
  edit_last_name_form = EditLastNameForm()

  if request.method == 'POST':
    if edit_last_name_form.validate_on_submit:
      current_edit.last_name = edit_last_name_form.last_name.data
      db.session.commit()
      flash('Successfully edited Last name!')

      return redirect(url_for('reg_user.my_account'))
    else:
      flash_errors(edit_last_name_form)

  return render_template("reg_user/edit_personal_info/edit_last_name.html",
                     title='My Account',
                     company_name=company_name,
                     year=year,
                     current_edit=current_edit,
                     edit_last_name_form=edit_last_name_form)  

@reg_user.route('/edit_telephone', methods=['GET', 'POST'])
@login_required
def edit_telephone():

  current_edit = User.query.filter_by(id = current_user.id).first()
  edit_telephone_form = EditTelephoneForm()

  if request.method == 'POST':
    if edit_telephone_form.validate_on_submit:
      current_edit.telephone = edit_telephone_form.telephone.data
      db.session.commit()
      flash('Successfully edited Telephone!')

      return redirect(url_for('reg_user.my_account'))
    else:
      flash_errors(edit_telephone_form)

  return render_template("reg_user/edit_personal_info/edit_telephone.html",
                     title='My Account',
                     company_name=company_name,
                     year=year,
                     current_edit=current_edit,
                     edit_telephone_form=edit_telephone_form)  

@reg_user.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():

  current_edit = User.query.filter_by(id = current_user.id).first()
  edit_password_form = EditPasswordForm()

  if request.method == 'POST':
    if edit_password_form.validate_on_submit:
      if current_edit is not None and current_edit.verify_password(edit_password_form.current_password.data):
        current_edit.password = edit_password_form.password.data
        db.session.commit()
        flash('Successfully edited Password!')

        return redirect(url_for('reg_user.my_account'))
      else:
        flash('Something went wrong!','error')

  return render_template("reg_user/edit_personal_info/edit_password.html",
                     title='My Account',
                     company_name=company_name,
                     year=year,
                     current_edit=current_edit,
                     edit_password_form=edit_password_form)  

@reg_user.route('/cancel_appointment', methods=['GET', 'POST'])
@login_required
def cancel_appointment():

  today = datetime(year, month, day)

  current_appointment = Appointment.query.filter(and_(Appointment.appointment_date >= today.strftime('%m/%d/%Y'),
                            Appointment.appointment_start_time > datetime.now().time().strftime('%H:%M'),
                            Appointment.attendance == "Pending",
                            Appointment.customer_id == current_user.id)).update(dict(attendance='Canceled'))
  db.session.commit()

  return redirect(url_for('reg_user.my_account'))

  return render_template("reg_user/my_account.html",
                       title='My Account',
                       company_name=company_name,
                       year=year)    