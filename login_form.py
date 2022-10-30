from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, validators
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional

from flask_login import current_user
from models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired()])
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=72)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        if not User.query.filter_by(username=username.data).first():
            raise ValidationError("Username %s doesn't exist." % username.data)
