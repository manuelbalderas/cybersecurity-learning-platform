from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField("Ingresar")


class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirma contraseña')
    submit = SubmitField("Registrar")

class FlagForm(FlaskForm):
    flag = StringField('Ingresa la bandera', validators=[DataRequired()])
    submit = SubmitField("Enviar")