from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, EqualTo, Regexp
 
from ..models import User

#This is the form that will handle user registrations.
class RegistrationForm(FlaskForm):
	first_name = StringField('First Name:', validators=[InputRequired(), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
	last_name = StringField('Last Name:', validators=[InputRequired(), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
	birth_date = DateField('Date of Birth:', format='%m/%d/%Y')
	email = StringField("Email", validators=[InputRequired(), Email()])
	telephone = StringField("Telephone:", [InputRequired(), Regexp('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', message='Only 10-digit phone numbers and prefixes are accepted.')])
	password = PasswordField('Password:', validators=[InputRequired(),EqualTo('confirm_password'), Regexp('^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Must contain 1 capital letter, 1 number & at least 8 characters')])
	confirm_password = PasswordField('Confirm Password:')
	submit = SubmitField("Register")

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
		    raise ValidationError('Email is already in use.')

#This is the form that will handle user logins.
class LoginForm(FlaskForm):
	email = StringField('Email address:', validators=[InputRequired(), Email()])
	password = PasswordField('Password:', validators=[InputRequired()])
	submit = SubmitField('Login')