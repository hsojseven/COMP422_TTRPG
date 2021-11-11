from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired, EqualTo, Length

# define our own FlaskForm subclass for our form
class LoginForm(FlaskForm):
  username = StringField("Username: ", validators=[InputRequired()])
  password = PasswordField("Password: ", 
      validators=[InputRequired(), Length(min=8, max=256)])
  submit = SubmitField("Submit")

class GameForm(FlaskForm):
  name = StringField("Name: ", validators=[InputRequired()])
  description = TextAreaField("Description: ", validators=[InputRequired()])
  submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
  username = StringField("Enter Username: ", validators=[InputRequired()])
  password = PasswordField("New Password: ", 
      validators=[InputRequired(), Length(min=8, max=256)])
  confirm_password = PasswordField("Confirm Password: ", 
      validators=[EqualTo('password')])
  submit = SubmitField("Register")
