from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

# define our own FlaskForm subclass for our form
class LoginForm(FlaskForm):
  username = StringField("Username: ", validators=[InputRequired()])
  submit = SubmitField("Submit")
