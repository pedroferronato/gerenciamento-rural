from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DateField


class ProducaoFinalizadasForm(FlaskForm):
    nome = StringField('Nome:')
    data_comeco = DateField('Data de início:')
    data_coleta = DateField('Data de coleta:')