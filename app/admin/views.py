from flask import abort, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required
from datetime import datetime

from . import admin
from .forms import AddServiceForm, RemoveServiceForm
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

@admin.route('/services', methods=['GET','POST'])
def services():
	"""
	Admin Interface - Services Function
	"""
	check_admin()

	#Instantiating forms
	add_service_form = AddServiceForm()
	remove_service_form = RemoveServiceForm()

	if request.method == 'POST':
		if add_service_form.validate_on_submit():
			service = Service(name=add_service_form.name.data.capitalize(),
							cost=add_service_form.cost.data.capitalize())
			try:
				# add service to the database
				db.session.add(service)
				db.session.commit()
				flash('You have successfully added a new service.', 'info')
			except:
				# in case service name already exists
				flash('Error: service name already exists.', 'error')

		# redirect to admin interface page
		return redirect(url_for('admin.services'))

	return render_template('admin/admin_interface.html',
								title="Admin_Interface",
								company_name=company_name,
								users=users_result,
								services=services_result,
								add_service_form=add_service_form,
								remove_service_form=remove_service_form)

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

	return render_template('admin/admin_interface.html',
								title="Admin_Interface",
								company_name=company_name,
								users=users_result,
								services=services_result,
								add_service_form=AddServiceForm(),
								remove_service_form=RemoveServiceForm())

