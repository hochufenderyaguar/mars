from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('team_leader', validators=[DataRequired()])
    job = StringField('job', validators=[DataRequired()])
    work_size = IntegerField('work_size', validators=[DataRequired()])
    collaborators = StringField('collaborators', validators=[DataRequired()])
    start_date = DateTimeField('start_date')
    end_date = DateTimeField('end_date')
    is_finished = BooleanField('is_finished')
    submit = SubmitField('submit')
