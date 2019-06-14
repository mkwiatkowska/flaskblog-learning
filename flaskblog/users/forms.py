from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectField)
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, ValidationError)
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken, choose different one')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists in db')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField(
        'Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username taken, choose different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already exists in db')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with this email, you must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class QuestionnaireForm(FlaskForm):
    genders = RadioField(choices=[('M', 'Męski'), ('F', 'Damski'), ('U', 'Unisex')])
    groups = RadioField(choices=[('1', 'Przyprawowej'),
     ('2', 'Kwiatowej'), ('3', 'Drzewnej'), ('4', 'Deserowej'),
     ('5', 'Ziołowej'), ('6', 'Animalnej'), ('7', 'Orientalnej'),
     ('8', 'Owocowej'), ('9', 'Cytrusowej'), ('10', 'Morskiej')])
    scents = RadioField(choices=[('1', 'Świeży'),
        ('2', 'Słodki'), ('3', 'Ciepły'), ('4', 'Gorzki'),
        ('5', 'Wytrawny'), ('6', 'Zimny')])
    submit = SubmitField('Submit')


class AddToFavourites(FlaskForm):
    perfume = SelectField('Perfume', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Submit')