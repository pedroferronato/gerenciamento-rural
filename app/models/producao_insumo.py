from app import db


class ProducaoInsumo(db.Model):
    __tablename__ = "producao_insumo"

    producao_id = db.Column(db.Integer, db.ForeignKey('producao.id'), nullable=False, primary_key=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumo.id'), nullable=False, primary_key=True)
    base = db.Column(db.Boolean(), default=False)