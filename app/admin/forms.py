from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, RadioField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, EqualTo, Regexp
 
from ..models import User, Service

#This is the form that will handle service additions
class AddServiceForm(FlaskForm):
  	name = StringField("Service Name:", [InputRequired()])
  	cost = StringField("Cost:", [InputRequired()])
  	submit = SubmitField("Submit")

#This is the form that will handle appointment scheduling.
class AdminAppointmentForm(FlaskForm):
  	appointment_date = StringField("Appointment Date:", [InputRequired()])
  	appointment_time = StringField("Appointment Time:", [InputRequired()])
  	customer = SelectField("Customer:", coerce=int, validators=[InputRequired()])
  	barber = SelectField("Barber:", coerce=int, validators=[InputRequired()])
  	service = SelectField("Service:", coerce=int, validators=[InputRequired()])
  	submit = SubmitField("Submit")

  	def __init__(self, *args, **kwargs):
  		super(AdminAppointmentForm, self).__init__(*args, **kwargs)
  		self.customer.choices = [(c.id, c.first_name + ' ' + c.last_name) for c in User.query.filter_by(role_id=1)]
  		self.barber.choices = [(b.id, b.first_name + ' ' + b.last_name) for b in User.query.filter_by(role_id=2)]
  		self.service.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name)]

#This is the form that will handle user additions by the admins.
class AddUserForm(FlaskForm):
	first_name = StringField('First Name:', validators=[InputRequired(), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
	last_name = StringField('Last Name:', validators=[InputRequired(), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
	birth_date = DateField('Date of Birth:', format='%m/%d/%Y')
	email = StringField("Email", validators=[InputRequired(), Email()])
	telephone = StringField("Telephone:", [InputRequired(), Regexp('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', message='Only 10-digit phone numbers and prefixes are accepted.')])
	password = PasswordField('Password:', validators=[InputRequired(),EqualTo('confirm_password'), Regexp('^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Must contain 1 capital letter, 1 number & at least 8 characters')])
	confirm_password = PasswordField('Confirm Password:')
	role_id = SelectField("Role:", choices=[('1', 'Customer'),('2', 'Barber')], validators=[InputRequired()])
	is_admin = RadioField('Grant Admin Privileges?', choices=[('True','Yes'),('False','No')], validators=[InputRequired()])
	submit = SubmitField("Register User")

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
		    raise ValidationError('Email is already in use.')