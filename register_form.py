from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(),
                    Length(min=3, max=15),
                    Regexp('^(?=.*[-+_!@#$%^&*., ?])')])
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=72)])
    submit = SubmitField('Submit')