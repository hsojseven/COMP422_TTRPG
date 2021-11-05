from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired

# define our own FlaskForm subclass for our form
class LoginForm(FlaskForm):
  username = StringField("Username: ", validators=[InputRequired()])
  submit = SubmitField("Submit")

class GameForm(FlaskForm):
  name = StringField("Name: ", validators=[InputRequired()])
  description = TextAreaField("Description: ", validators=[InputRequired()])
  submit = SubmitField("Submit")
