from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(),
                    Length(min=3, max=15)])
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=72)])
    submit = SubmitField('Submit')