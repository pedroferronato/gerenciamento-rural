from app import db
import math


class Insumo(db.Model):
    __tablename__ = "insumo"

    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('movimentador.id'), nullable=False)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    quantidade_estocada = db.Column(db.Float)
    valor_unitario = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    utilidade = db.Column(db.String(100), nullable=False)
    unidade_medida = db.Column(db.String(50))


    def valor_final_formatado(self):
        return 'R$ {:.2f}'.format(self.valor_total)


    def valor_unitario_formatado(self):
        return 'R$ {:.2f}'.format(self.valor_unitario)


    def quantidade_estocada_formatada(self):
        if self.quantidade_estocada.is_integer():
            return "{} {}".format(int(self.quantidade_estocada), self.unidade_medida)
        return "{} {}".format(self.quantidade_estocada, self.unidade_medida)


    def quantidade_formatada(self):
        if self.quantidade.is_integer():
            return "{} {}".format(int(self.quantidade), self.unidade_medida)
        return "{} {}".format(self.quantidade, self.unidade_medida)
