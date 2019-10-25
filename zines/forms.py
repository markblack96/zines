from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, IntegerField, StringField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, ValidationError
from wtforms.widgets import HiddenInput


class CreatePost(FlaskForm):
    delta = HiddenField(
        'delta',
        validators=[Length(0, 255)],
    )

    content_length = IntegerField(
        label='',
        validators=[
            NumberRange(2, 255, "Please post something longer/shorter")
        ],
        widget=HiddenInput()
    )

    submit = SubmitField('Create Post')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
