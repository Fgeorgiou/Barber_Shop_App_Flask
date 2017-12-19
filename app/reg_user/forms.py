from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, EqualTo, Regexp
 
from ..models import User, Service

#This is the form that will handle appointment scheduling.
class UserAppointmentForm(FlaskForm):
  	appointment_date = StringField("Appointment Date:", [InputRequired()])
  	appointment_time = StringField("Appointment Time:", [InputRequired()])
  	barber = SelectField("Barber", coerce=int, validators=[InputRequired()])
  	service = SelectField("Service:", coerce=int, validators=[InputRequired()])
  	submit = SubmitField("Submit")

  	def __init__(self, *args, **kwargs):
  		super(UserAppointmentForm, self).__init__(*args, **kwargs)
  		self.barber.choices = [(a.id, a.first_name + ' ' + a.last_name) for a in User.query.filter_by(role_id=2)]
  		self.service.choices = [(a.id, a.name) for a in Service.query.order_by(Service.name)]

#This is the form that will handle email edits.
class EditEmailForm(FlaskForm):

	email = StringField("New Email", validators=[InputRequired(), Email(), EqualTo('confirm_email'), Regexp("^(([^<>()\[\]\\.,;:\s@']+(\.[^<>()\[\]\\.,;:\s@']+)*)|('.+'))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$")])
	confirm_email = StringField('Confirm New Email:')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')

#This is the form that will handle first name edits.
class EditFirstNameForm(FlaskForm):

	first_name = StringField('New First Name:', validators=[InputRequired(), EqualTo('confirm_first_name'), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
	confirm_first_name = StringField('Confirm New First Name:')

#This is the form that will handle last name edits.	
class EditLastNameForm(FlaskForm):

	last_name = StringField('New Last Name:', validators=[InputRequired(), EqualTo('confirm_last_name'), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
	confirm_last_name = StringField('Confirm New Last Name:')

#This is the form that will handle password edits.
class EditPasswordForm(FlaskForm):

	current_password = PasswordField('Current Password:', validators=[InputRequired()])
	password = PasswordField('New Password:', validators=[InputRequired(),EqualTo('confirm_password'), Regexp('^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Must contain 1 capital letter, 1 number & at least 8 characters')])
	confirm_password = PasswordField('Confirm New Password:')

#This is the form that will handle telephone edits.	
class EditTelephoneForm(FlaskForm):

	telephone = StringField("New Telephone:", [InputRequired(), EqualTo('confirm_telephone'), Regexp('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', message='Only 10-digit phone numbers and prefixes are accepted.')])
	confirm_telephone = StringField('Confirm New Telephone:')

