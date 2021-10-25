from flask_wtf import FlaskForm
from wtforms import DateField, SelectField
from wtforms.validators import DataRequired, Length


class CompraHistoricoForm(FlaskForm):
    fornecedor = SelectField('Fornecedor:')
    data_inicio = DateField('Data inicial:', format='%d/%m/%Y')
    data_final = DateField('Data final:', format='%d/%m/%Y')
