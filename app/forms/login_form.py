from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    usuario = StringField('Usuário:', 
                        validators=[DataRequired(message='Insira seu usuário')])
    senha = PasswordField('Senha:',
                        validators=[DataRequired(message='Insira sua senha'), Length(min=3, message='Senha muito curta')])
