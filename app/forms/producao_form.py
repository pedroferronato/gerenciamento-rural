from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, NumberRange


class ProducaoForm(FlaskForm):
    nome = StringField('Nome identificador:', 
                            validators=[DataRequired(message="Insira uma nome para identificar a produção")])
    quantidade = FloatField('Quantidade do produto:', 
                            validators=[NumberRange(min=0, max=1000000, message="Insira um valor válido")])
    data = StringField('Data de início:',
                            default=date.today().strftime('%d/%m/%Y'),
                            validators=[DataRequired(message="Insira a data de início da produção")])
