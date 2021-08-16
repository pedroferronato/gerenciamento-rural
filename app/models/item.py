from app import db


class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    producao_id = db.Column(db.Integer, db.ForeignKey('producao.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    valor_unitario = db.Column(db.Float)
    validade = db.Column(db.Date(), nullable=False)
    unidade_medida = db.Column(db.String(5), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
