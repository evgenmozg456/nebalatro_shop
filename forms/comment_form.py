from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    # rate = IntegerField("Поставьте оценку", validators=[DataRequired()])

    text = TextAreaField("Напишите комментарий", validators=[DataRequired()])
    # text1 = StringField("Напишите комментарий", validators=[DataRequired()])
    send = SubmitField('Отправить')
