from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email = EmailField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[Length(min=6), EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Email already exists.')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log In')

class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Purchase')

class SellForm(FlaskForm):
    submit = SubmitField(label='Sell')