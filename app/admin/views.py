from flask import abort, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required
from datetime import datetime

from . import admin
from .forms import AddServiceForm, AddUserForm
from .. import db
from ..models import *

#global variables
company_name = {'name' : 'LaKosta'} # Test
year = datetime.now().year

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
								add_user_form=AddUserForm())


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
								add_service_form=AddServiceForm())



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

@admin.route('/mark_unattended/<int:id>', methods=['GET', 'POST'])
@login_required
def mark_unattended(id):
    #Mark Appointments as Unattended
    check_admin()

    appointment = Appointment.query.filter_by(id=id).update(dict(attendance=False))
    db.session.commit()
    flash('You have successfully marked an appointment as unattended!', 'info')

    # redirect to admin interface
    return redirect(url_for('admin.admin_interface'))

    return render_template('admin/admin_interface.html')



@admin.route('/admin_interface', methods=['GET','POST'])
@login_required
def admin_interface():
	"""
	Admin Interface - Users View
	"""
	check_admin()

	#Query the database for the required info
	users_result = User.query.all()
	services_result = Service.query.all()
	appointments_result = Appointment.query.all()

	return render_template('admin/admin_interface.html',
								title="Admin Interface",
								company_name=company_name,
								users=users_result,
								services=services_result,
								appointments=appointments_result,
								add_service_form=AddServiceForm(),
								add_user_form=AddUserForm())



# @admin.route('/appointments', methods=['GET','POST'])
# @login_required
# def appointments():
# 	"""
# 	Admin Interface - Users View
# 	"""
# 	check_admin()

# 	#Query the database for the required info
# 	users = User.query.all()

# 	if request.method == 'POST':
# 		if add_service_form.validate_on_submit():
# 			service = Service(name=add_service_form.name.data,
# 							cost=add_service_form.cost.data)
# 			try:
# 				# add service to the database
# 				db.session.add(service)
# 				db.session.commit()
# 				flash('You have successfully added a new service.', 'info')
# 			except:
# 				# in case service name already exists
# 				flash('Error: service name already exists.', 'error')

# 		# redirect to admin interface page
# 		return redirect(url_for('admin.appointments'))

# 	return render_template('admin/appointments.html',
# 								title="Admin_Interface",
# 								company_name=company_name,
# 								users=users)

