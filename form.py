from flask_wtf import Form
from wtforms import TextField, PasswordField, RadioField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = TextField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class GenderForm(Form):
	gender = RadioField('Gender', choices=[('female','Female'),('male','Male')])