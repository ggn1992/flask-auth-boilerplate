from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

class LoginRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class RegisterUserRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class PasswordChangeRequestForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat New Password", validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField("Change Password")

class SetNewPasswordForm(FlaskForm):
    new_password = PasswordField("New Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat New Password", validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField("Reset Password")
