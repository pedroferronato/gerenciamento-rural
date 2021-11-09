from app import db
from app.models.insumo import Insumo


class ProducaoInsumo(db.Model):
    __tablename__ = "producao_insumo"

    producao_id = db.Column(db.Integer, db.ForeignKey('producao.id'), nullable=False, primary_key=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable=False, primary_key=True)
    quantidade_aplicada = db.Column(db.Float)
    data = db.Column(db.Date())
    base = db.Column(db.Boolean(), default=False)


    def get_insumo_relacionado(self):
        return Insumo.query.filter_by(id=self.insumo_id).first()
