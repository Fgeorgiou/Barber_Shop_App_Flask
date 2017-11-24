from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Email
 
#This is the form that will be staged in the contact page.
class ContactForm(FlaskForm):
  	email = StringField("Email", [InputRequired(), Email("Please enter a valid email format")])
  	subject = StringField("Subject", [InputRequired()])
  	message = TextAreaField("Message", [InputRequired()])
  	submit = SubmitField("Send")

