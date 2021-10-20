from app import db


class Compra(db.Model):
    __tablename__ = "compra"

    id = db.Column(db.Integer, primary_key=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    data = db.Column(db.Date(), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable=False, primary_key=True)
    movimentador_id = db.Column(db.Integer, db.ForeignKey('movimentador.id'), nullable=False, primary_key=True)
    quantidade = db.Column(db.Float, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
