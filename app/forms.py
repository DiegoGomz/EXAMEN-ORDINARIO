from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class NoteForm(FlaskForm):
    title = StringField("Titulo", validators=[DataRequired()])
    body = StringField("Cuerpo", validators=[DataRequired()])
    submit = SubmitField("Crear")

class PublicacionForm(FlaskForm):
    title = StringField("Titulo", validators=[DataRequired()])
    body = StringField("Cuerpo", validators=[DataRequired()])
    submit = SubmitField("Crear")