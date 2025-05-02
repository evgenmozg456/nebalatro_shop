from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RedactForm(FlaskForm):
    avatar = FileField('аватар')
    name = StringField('Имя пользователя')
    about = TextAreaField("о себе")
    submit = SubmitField('изменить')
