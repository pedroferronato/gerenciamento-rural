from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DateField


class EstoqueForm(FlaskForm):
    nome = StringField('Nome:')
    validade = DateField('Validade:')
