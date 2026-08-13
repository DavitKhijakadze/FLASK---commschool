from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("მომხმარებლის სახელი", validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField("პაროლი", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("დაადასტურეთ პაროლი", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("რეგისტრაცია")

class LoginForm(FlaskForm):
    username = StringField("მომხმარებლის სახელი", validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired()])
    submit = SubmitField("შესვლა")

class NoteForm(FlaskForm):
    title = StringField("სათაური", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("შინაარსი", validators=[DataRequired()])
    submit = SubmitField("შენახვა")
    