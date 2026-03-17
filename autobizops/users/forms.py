# autobizops/users/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField, SubmitField, ValidationError
from wtforms.validators import Email, DataRequired, EqualTo
from autobizops.models import User
import email_validator


class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords must match")])
    pass_confirm = PasswordField('Confirm Password: ', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail has been registered already.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username has been already taken.')


class LoginForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
