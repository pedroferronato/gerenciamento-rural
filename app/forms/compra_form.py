from datetime import date
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField
from wtforms.validators import DataRequired, Length


class CompraForm(FlaskForm):
    insumo = StringField('Insumo:', validators=[DataRequired('Insira o insumo adicionado'), Length(min=-1, max=200, message="Por favor, não ultrapasse 200 caracteres")])
    fornecedor = SelectField('Fornecedor:', validators=[DataRequired('Insira o fornecedor')])
    finalidade = SelectField('Finalidade:', validators=[DataRequired('Insira a finalidade'), Length(min=-1, max=100, message="Por favor, não ultrapasse 100 caracteres")])
    data = DateField('Data da compra:', format='%d/%m/%Y', default=date.today(), validators=[DataRequired('Insira a data da compra')])
    valor_unitario = StringField('Valor unitário (R$):', validators=[DataRequired('Insira o valor de cada unidade comprada')])
    quantidade = StringField('Quantidade:', validators=[DataRequired('Insira a quantidade')])
    unidade = StringField('Unidade de medida:', default='Unidade', validators=[DataRequired('Insira a unidade do insumo comprado (unidade, Kg, Litros)')])
    desconto = StringField('Desconto:', validators=[Length(min=0, max=50, message="Por favor, não ultrapasse 50 caracteres")])
    valor_total = StringField('Valor total (R$):', validators=[DataRequired('Insira o valor total da compra')])
