from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField


class ProducaoFinalizadasForm(FlaskForm):
    nome = StringField('Nome:')
    data_comeco = StringField('Data de início:')
    data_coleta = StringField('Data de coleta:')