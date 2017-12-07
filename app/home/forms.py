from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email
 
from ..models import User, Service
 
#This is the form that will handle contact requests.
class ContactForm(FlaskForm):
  	email = StringField("Email", [InputRequired(), Email("Please enter a valid email format")])
  	subject = StringField("Subject", [InputRequired()])
  	message = TextAreaField("Message", [InputRequired()])
  	submit = SubmitField("Send")

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
