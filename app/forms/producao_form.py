from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FloatField, DateField
from wtforms.validators import DataRequired, NumberRange


class ProducaoForm(FlaskForm):
    produto = SelectField('Produto:', 
                            validators=[DataRequired(message="Insira o produto da criação (Plantado ou posto)")])
    nome = StringField('Nome identificador:', 
                            validators=[DataRequired(message="Insira uma nome para identificar a produção")])
    quantidade = FloatField('Quantidade do produto:', 
                            validators=[NumberRange(min=0, max=1000000, message="Insira um valor válido")])
    data = DateField('Data de início:', format='%d/%m/%Y', 
                            default=date.today(),
                            validators=[DataRequired(message="Insira a data de início da produção")])
