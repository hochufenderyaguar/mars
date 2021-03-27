from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class DepartmentForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    chief = IntegerField('chief', validators=[DataRequired()])
    members = StringField('members', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    submit = SubmitField('submit')
