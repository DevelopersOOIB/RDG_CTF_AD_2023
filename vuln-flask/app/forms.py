from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, ValidationError, Length

from app.models import User


class FlagForm(FlaskForm):
    name = StringField('Flag', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')],
                              render_kw={"placeholder": "Repeat password"})
    submit = SubmitField('Register')

    def validate_username(self, username) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class ProfileForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    bio = TextAreaField('Bio', validators=[Length(max=250)])
    submit = SubmitField('Save')

    def validate_username(self, username) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')