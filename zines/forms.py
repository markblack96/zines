from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, IntegerField
from wtforms.validators import Length, NumberRange
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
