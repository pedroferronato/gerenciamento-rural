from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class ProdutorCadastroForm(FlaskForm):
    nome = StringField('Nome:', validators=[DataRequired(message='Insira seu nome')])
    login = StringField('Usuário:', 
                        validators=[DataRequired(message='Insira um nome de usuário para acessar o sistema'),
                                    Length(min=5, max=20, message='Insira um usuário com um número de dígitos entre (5 e 20)')])
    senha = PasswordField('Senha:', 
                        validators=[DataRequired(message='Insira uma senha'), 
                                    Length(min=6, max=16, message='Insira uma senha com um número de dígitos entre (6 e 16)')])
    confirmar_senha = PasswordField('Confirmar senha:',
                        validators=[DataRequired(message='Insira a confirmação da senha'), 
                                    Length(min=6, max=16, message='Insira uma senha com um número de dígitos entre (6 e 16)'), 
                                    EqualTo('senha', message='As senhas devem coincidir')])