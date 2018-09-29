from flask_wtf import FlaskForm
from wtforms import (
  StringField,
  PasswordField,
  SubmitField,
  BooleanField,
  TextAreaField
)
from wtforms.validators import (
  DataRequired,
  Length,
  Email,
  EqualTo,
  ValidationError
)
from .models import User

class RegisterForm(FlaskForm):
  username = StringField('Username', validators = [DataRequired(), Length(min=3, max=20)])
  email = StringField('Email', validators = [DataRequired(), Email()])
  password = PasswordField('Password', validators = [DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  # Custom Validations
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is already taken!')

  def validate_email(self, email):
    email = User.query.filter_by(email=email.data).first()
    if email:
      raise ValidationError('That email is already being used!')

class LoginForm(FlaskForm):
  username = StringField('Username', validators = [DataRequired()])
  password = PasswordField('Password', validators = [DataRequired()])
  submit = SubmitField('Login')


class PostForm(FlaskForm):
  title = StringField('Title', validators = [DataRequired()])
  content = TextAreaField('Content', validators = [DataRequired()])
  submit = SubmitField('Post')