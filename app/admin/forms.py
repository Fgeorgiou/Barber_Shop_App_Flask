from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Email
 
#This is the form that will handle service additions
class AddServiceForm(FlaskForm):
  	name = StringField("Service Name:", [InputRequired()])
  	cost = StringField("Cost:", [InputRequired()])
  	submit = SubmitField("Submit")

#This is the form that will service removals
class RemoveServiceForm(FlaskForm):
  	name = StringField("Service Name:", [InputRequired()])
  	submit = SubmitField("Submit")