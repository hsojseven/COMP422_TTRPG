from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
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

  class CharacterForm(FlaskForm):
    name = StringField("Enter Name: ", validators=[InputRequired()])
    strength = IntegerField("Enter Strength: ", validators=[InputRequired(), Length(min=0, max=20)]),
    dexterity = IntegerField("Enter Dexterity: ", validators=[InputRequired(), Length(min=0, max=20)]),
    constitution = IntegerField("Enter Constitution: ", validators=[InputRequired(), Length(min=0, max=20)]),
    intelligence = IntegerField("Enter Intelligence: ", validators=[InputRequired(), Length(min=0, max=20)]),
    wisdom = IntegerField("Enter Wisdom: ", validators=[InputRequired(), Length(min=0, max=20)]),
    charisma = IntegerField("Enter Charisma: ", validators=[InputRequired(), Length(min=0, max=20)]),
    submit = SubmitField("Register")


