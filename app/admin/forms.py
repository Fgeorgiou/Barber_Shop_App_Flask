from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Email
 
#This is the form that will handle service additions
class AddServiceForm(FlaskForm):
  	name = StringField("Service Name:", [InputRequired()])
  	cost = StringField("Cost:", [InputRequired()])
  	submit = SubmitField("Submit")

#This is the form that will handle user registrations. TODO implement an edit system for admins
# class EditForm(FlaskForm):
# 	first_name = StringField('First Name:', validators=[InputRequired(), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
# 	last_name = StringField('Last Name:', validators=[InputRequired(), Regexp('^[a-zA-Z ]*$', message='Only letters and white space allowed')])
# 	birth_date = DateField('Date of Birth:', format='%m/%d/%Y')
# 	email = StringField("Email", validators=[InputRequired(), Email()])
# 	telephone = StringField("Telephone:", [InputRequired(), Regexp('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', message='Only 10-digit phone numbers and prefixes are accepted.')])
# 	password = PasswordField('Password:', validators=[InputRequired(),EqualTo('confirm_password'), Regexp('^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Must contain 1 capital letter, 1 number & at least 8 characters')])
# 	confirm_password = PasswordField('Confirm Password:')
# 	submit = SubmitField("Register")

# 	def validate_email(self, field):
# 		if User.query.filter_by(email=field.data).first():
# 		    raise ValidationError('Email is already in use.')