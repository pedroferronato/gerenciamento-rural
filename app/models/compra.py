from app import db
from app.models.insumo import Insumo
from app.models.movimentador import Movimentador


class Compra(db.Model):
    __tablename__ = "compra"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    data = db.Column(db.Date(), nullable=False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable=False, primary_key=True)
    movimentador_id = db.Column(db.Integer, db.ForeignKey('movimentador.id'), nullable=False, primary_key=True)
    desconto = db.Column(db.String(50))

    
    def get_insumo(self):
        return Insumo.query.filter_by(id=self.insumo_id).first()

    def get_fornecedor(self):
        return Movimentador.query.filter_by(id=self.movimentador_id).first()
