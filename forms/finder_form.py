from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField


class FindForm(FlaskForm):
    game = StringField()
    submit = SubmitField('Войти')