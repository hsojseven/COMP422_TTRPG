from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired, EqualTo, Length, NumberRange

# define our own FlaskForm subclass for our form
class LoginForm(FlaskForm):
  username = StringField(validators=[InputRequired()])
  password = PasswordField(validators=[InputRequired(), Length(min=8, max=256)])
  submit = SubmitField("Login")
  
class GameForm(FlaskForm):
  name = StringField(validators=[InputRequired()])
  description = TextAreaField(validators=[InputRequired()])
  submit = SubmitField("Add")

class RegisterForm(FlaskForm):
  username = StringField(validators=[InputRequired()])
  password = PasswordField(validators=[InputRequired(), Length(min=8, max=256)])
  confirm_password = PasswordField(validators=[EqualTo('password')])
  submit = SubmitField("Register")

class CharacterForm(FlaskForm):
  integer_message = "Value must be between 0 and 20"
  name = StringField(validators=[InputRequired()])
  strength = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  dexterity = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  constitution = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  intelligence = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  wisdom = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  charisma = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=20, message=integer_message)])
  submit = SubmitField("Add")