from app import db


class Insumo(db.Model):
    __tablename__ = "insumo"

    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('movimentador.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    valor_unitario = db.Column(db.Float)
    validade = db.Column(db.Date(), nullable=False)
    utilidade = db.Column(db.String(50), nullable=False)
    unidade_medida = db.Column(db.String(5), nullable=False)