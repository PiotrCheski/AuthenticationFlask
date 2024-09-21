from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from authenticationflask.models import User

def password_complexity_check(form, field):
    password = field.data
    if not any(char.islower() for char in password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not any(char.isupper() for char in password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one number.')
    if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in password):
        raise ValidationError('Password must contain at least one special character.')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=64), password_complexity_check])

    confirmation_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a diffrent one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.') 


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


