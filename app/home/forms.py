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
