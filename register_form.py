from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo

class RegisterForm(FlaskForm):
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
        validators=[
            InputRequired(), Length(min=8, max=72),
            Regexp(
                "^(?=[^A-Z]*[A-Z])(?=[^0-9]*[0-9])",
                0,
                "Password must include atleast one uppercase letter, one lowercase letter and a digit."
            )
        ])
    cpassword = PasswordField(
        'Confirm password',
        validators=[
            InputRequired(),
            Length(min=8, max=72),
            EqualTo("password", message="Passwords not matching")
        ]
    )
    submit = SubmitField('Submit')