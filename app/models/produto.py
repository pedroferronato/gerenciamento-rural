from app import db


class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    producao_id = db.Column(db.Integer, db.ForeignKey('producao.id'), nullable=False)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    valor_unitario = db.Column(db.Float)
    validade = db.Column(db.Date())
    unidade_medida = db.Column(db.String(50), nullable=False)

    def quantidade_formatada(self):
        if self.quantidade.is_integer():
            return "{} {}".format(int(self.quantidade), self.unidade_medida)
        return "{} {}".format(self.quantidade, self.unidade_medida)