from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length


class PropriedadeCadastroForm(FlaskForm):
    nome = StringField('Nome da propriedade:', 
                        validators=[DataRequired(message="Insira o nome da propriedade"),
                                    Length(min=6, max=70, 
                                            message="O nome deve ter no mínimo 6 dígitos e no máximo 70 dígitos")])
    endereco = StringField('Endereço:',
                            validators=[DataRequired(message="Insira o endereço")])
    area = IntegerField("Área:")
    contato = StringField("Contato:")
