from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired, EqualTo, Length, NumberRange

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

class CharacterForm(FlaskForm):
  integer_message = "Value must be between 0 and 20"
  name = StringField("Character Name: ", validators=[InputRequired()])
  strength = IntegerField("Strength (between 0 and 20): ", validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  dexterity = IntegerField("Dexterity (between 0 and 20): ", validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  constitution = IntegerField("Constitution (between 0 and 20): ", validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  intelligence = IntegerField("Intelligence (between 0 and 20): ", validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  wisdom = IntegerField("Wisdom (between 0 and 20): ", validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  charisma = IntegerField("Charisma (between 0 and 20): ", validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  submit = SubmitField("Register")