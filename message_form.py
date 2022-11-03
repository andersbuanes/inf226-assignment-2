from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class MessageForm(FlaskForm):
    message: StringField(
        'Message',
        validators=[
            InputRequired(),
            Length(max=300),
        ]
    )
    recipients: StringField(
        'Recipients',
        validators=[
            InputRequired(),
            Length(max=300),
        ]
    )
    submit = SubmitField('Send')
    