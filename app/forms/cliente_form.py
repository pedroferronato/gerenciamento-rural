from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ClienteForm(FlaskForm):
    nome = StringField('Nome:', validators=[
        DataRequired(message="Insira o nome do cliente"),
        Length(min=3, max=60, message="O nome deve ter no mínimo 3 dígitos e no máximo 60 dígitos")
    ])
    contato = StringField('Contato:')
    endereco = StringField('Endereço:')
