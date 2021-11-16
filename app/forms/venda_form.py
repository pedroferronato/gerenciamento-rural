from datetime import date
from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, StringField
from wtforms.validators import DataRequired, Length


class VendaForm(FlaskForm):
    data = DateField('Data da venda:', format='%d/%m/%Y', default=date.today(), validators=[DataRequired('Insira a data de venda')])
    quantidade = FloatField('Quantidade:', validators=[DataRequired('Insira a quantidade vendida')])
    valor_total = FloatField('Valor total:', validators=[DataRequired('Insira o valor total da venda, ou deixe o cálculo automático')])
    desconto = StringField('Desconto:', validators=[Length(min=0, max=50, message="Por favor, não ultrapasse 50 caracteres")])
    valor_unitario = FloatField('Valor unitário:', validators=[DataRequired('Insira ')])
    