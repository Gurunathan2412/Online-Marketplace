from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, u):
        user = User.query.filter_by(username=u.data).first()
        if user:
            raise ValidationError("Username already existed")

    def validate_email(self, e):
        email = User.query.filter_by(email=e.data).first()
        if email:
            raise ValidationError("Email already existed")

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Submit')


class Login(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class Purchase(FlaskForm):
    submit = SubmitField(label='Purchase Item')


class Sell(FlaskForm):
    submit = SubmitField(label='Sell Item')
