from flask_wtf import FlaskForm
from wtforms import StringField
from datetime import date

class CompraHistoricoForm(FlaskForm):
    data_inicio = StringField('Data inicial:', default=date.today().strftime('%d/%m/%Y'))
    data_final = StringField('Data final:')
