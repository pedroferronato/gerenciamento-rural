from app import db


class Compra(db.Model):
    __tablename__ = "compra"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    data = db.Column(db.Date(), nullable=False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable=False, primary_key=True)
    movimentador_id = db.Column(db.Integer, db.ForeignKey('movimentador.id'), nullable=False, primary_key=True)
    desconto = db.Column(db.String(50))
