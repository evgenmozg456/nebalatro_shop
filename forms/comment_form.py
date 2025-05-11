from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

# форма для комментариев
class CommentForm(FlaskForm):
    text = TextAreaField("Напишите комментарий", validators=[DataRequired()])
    send = SubmitField('Отправить')
