from flask import abort, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from sqlalchemy import and_

from . import admin
from .forms import AddServiceForm, AdminAppointmentForm, AddUserForm
from .. import db
from ..models import *

#global variables
company_name = {'name' : 'LaKosta'}
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day

def check_admin():
	"""
	Prevent non_admin user from accessing admin content
	This function will be called inside all the admin views
	"""
	if not current_user.is_admin:
		abort(403)

@admin.route('/add_service', methods=['GET','POST'])
@login_required
def add_service():
    #Create Services
	check_admin()

	#Instantiating forms
	add_service_form = AddServiceForm()

	if request.method == 'POST':
		if add_service_form.validate_on_submit():
			service_to_add = Service(name=add_service_form.name.data.capitalize(),
							cost=add_service_form.cost.data)
			try:
				# add service to the database
				db.session.add(service_to_add)
				db.session.commit()
				flash('You have successfully added a new service.', 'info')
			except:
				# in case service name already exists
				flash('Error: service name already exists.', 'error')

			return redirect(url_for('admin.admin_interface'))

	return render_template('admin/admin_interface.html',
								add_service_form=add_service_form,
								add_user_form=AddUserForm(),
								add_appointment_form=AdminAppointmentForm())


@admin.route('/add_user', methods=['GET','POST'])
@login_required
def add_user():
    #Create Users
	check_admin()

	#Instantiating forms
	add_user_form = AddUserForm()

	if request.method == 'POST':
		if add_user_form.validate_on_submit():
			is_admin_val = None

			if add_user_form.is_admin.data == 'True':
				is_admin_val = True
			else:
				is_admin_val = False
			user_to_add = User(first_name=add_user_form.first_name.data.capitalize(),
                        	last_name=add_user_form.last_name.data.capitalize(),
                        	birth_date=add_user_form.birth_date.data,
                       		email=add_user_form.email.data,
                        	telephone=add_user_form.telephone.data,
                        	password=add_user_form.password.data,
                        	role_id=add_user_form.role_id.data,
                        	is_admin=is_admin_val)
			try:
				# add service to the database
				db.session.add(user_to_add)
				db.session.commit()
				flash('You have successfully added a new user!', 'info')
			except:
				# in case user already exists
				flash('Error: user already exists.', 'error')

			return redirect(url_for('admin.admin_interface'))

	return render_template('admin/admin_interface.html',
								add_user_form=add_user_form,
								add_service_form=AddServiceForm(),
								add_appointment_form=AdminAppointmentForm())


@admin.route('/add_appointment', methods=['GET','POST'])
@login_required
def add_appointment():
    #Create Users
	check_admin()

	#Instantiating forms
	add_appointment_form = AdminAppointmentForm()

	if request.method == 'POST':
		if add_appointment_form.validate_on_submit():
			'''
			!Criteria for an appointment to be valid!
			a. Cant make an appointment on any day before today
			b. Cant make an appointment on a time before now
			c. User cant have more than 1 active appointment to avoid intentional system overload
			'''
			#time variables neccesary for calculating appointment credibility
			today = datetime(year, month, day)
			time_string = add_appointment_form.appointment_time.data

			#Criteria a check
			if add_appointment_form.appointment_date.data < today.strftime('%m/%d/%Y'):
				flash ("Appointment can't be scheduled for a date before today" + today.strftime('%m/%d/%Y'), 'error')
			#Criteria b check
			elif add_appointment_form.appointment_date.data == today.strftime('%m/%d/%Y') and time_string < datetime.now().time().strftime('%H:%M'):
				flash ("Appointment can't be scheduled for a time sooner than now! - Current Time: " + datetime.now().time().strftime('%H:%M'), 'error')
			else:
				#Time calculation function for appointment's end
				def nextTime(time, minutestoadd):
					base_time = datetime.strptime(time, "%H:%M")
					minutesobj = timedelta(minutes = minutestoadd)
					newtime = base_time + minutesobj
					return newtime.strftime('%H:%M')

				#calculate the appointment cost based on the user's selection
				service_to_evaluate = Service.query.filter_by(id=add_appointment_form.service.data).first()
				service_cost = service_to_evaluate.cost

				#Database query for appointment
				appointment = Appointment(appointment_date = add_appointment_form.appointment_date.data,
					appointment_start_time = add_appointment_form.appointment_time.data,
					appointment_end_time = nextTime(time_string, 30),
					appointment_cost = service_cost,
					customer_id = add_appointment_form.customer.data,
					barber_id = add_appointment_form.barber.data,
					service_id = add_appointment_form.service.data,
					made_by = current_user.id,
					timestamp = datetime.now())

				db.session.add(appointment)
				db.session.commit()
				flash('Appointment was scheduled successfully!', 'info')

				# redirect to the login page
				return redirect(url_for('admin.admin_interface'))
		else:
			flash_errors(appointment_form)
		return redirect(url_for('admin.admin_interface'))

	return render_template("admin/admin_interface.html",
	title='Admin_Interface',
	company_name=company_name,
	year=year,
	add_appointment_form=add_appointment_form,
	add_service_form=AddServiceForm(),
	add_user_form=AddUserForm())


@admin.route('/delete_service/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_service(id):
    #Delete Services
    check_admin()

    service_to_delete = Service.query.get_or_404(id)
    db.session.delete(service_to_delete)
    db.session.commit()
    flash('You have successfully deleted a service.', 'info')

    # redirect to admin interface
    return redirect(url_for('admin.admin_interface'))

    return render_template('admin/admin_interface.html')


@admin.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    #Delete Users
    check_admin()

    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('You have successfully deleted a user.', 'info')

    # redirect to admin interface
    return redirect(url_for('admin.admin_interface'))

    return render_template('admin/admin_interface.html')

@admin.route('/mark_attended/<int:id>', methods=['GET', 'POST'])
@login_required
def mark_attended(id):
    #Mark Appointments as Unattended
    check_admin()

    appointment = Appointment.query.filter_by(id=id).update(dict(attendance='Attended'))
    db.session.commit()
    flash('You have successfully marked an appointment as attended!', 'info')

    # redirect to admin interface
    return redirect(url_for('admin.admin_interface'))

    return render_template('admin/admin_interface.html')


@admin.route('/mark_unattended/<int:id>', methods=['GET', 'POST'])
@login_required
def mark_unattended(id):
    #Mark Appointments as Unattended
    check_admin()

    appointment = Appointment.query.filter_by(id=id).update(dict(attendance='Unattended'))
    db.session.commit()
    flash('You have successfully marked an appointment as unattended!', 'info')

    # redirect to admin interface
    return redirect(url_for('admin.admin_interface'))

    return render_template('admin/admin_interface.html')

@admin.route('/mark_canceled/<int:id>', methods=['GET', 'POST'])
@login_required
def mark_canceled(id):
    #Mark Appointments as Unattended
    check_admin()

    appointment = Appointment.query.filter_by(id=id).update(dict(attendance='Canceled'))
    db.session.commit()
    flash('You have successfully marked an appointment as canceled!', 'info')

    # redirect to admin interface
    return redirect(url_for('admin.admin_interface'))

    return render_template('admin/admin_interface.html')


@admin.route('/admin_interface', methods=['GET','POST'])
@login_required
def admin_interface():
	#Admin Interface - Users View
	check_admin()

	today = datetime(year, month, day)

	#Query the database for the required info
	#Query for collecting the users
	users_result = User.query.all()
	#Query for collecting the roles
	roles_result = Role.query.all()
	#Query for collecting the services
	services_result = db.session.query(Service).order_by(Service.name)
	#Query for collecting the appointments in descending order
	appointments_result = Appointment.query.all()
	#Query for getting the appointments with a date of today and a time later than now
	upcoming_appointments = db.session.query(Appointment).filter(and_(Appointment.appointment_date >= today.strftime('%m/%d/%Y'),
														Appointment.appointment_start_time > datetime.now().time().strftime('%H:%M'),
														Appointment.attendance == "Pending"))

	appointments_formatted = Appointment.query.join(User, Appointment.customer_id == User.id)


	return render_template('admin/admin_interface.html',
								title="Admin Interface",
								company_name=company_name,
								users=users_result,
								roles=roles_result,
								services=services_result,
								appointments=appointments_result,
								upcoming_appointments=upcoming_appointments,
								add_appointment_form=AdminAppointmentForm(),
								add_service_form=AddServiceForm(),
								add_user_form=AddUserForm())


