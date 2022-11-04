from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            InputRequired(),
            Length(min=3, max=15),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.\-]*$",
                0,
                "Username can only contain letters, numbers, dots or underscores"
            )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=72)])
    submit = SubmitField('Submit')