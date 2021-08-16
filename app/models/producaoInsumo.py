from app import db


class ProducaoInsumo(db.Model):
    __tablename__ = "producao_insumo"

    producao_id = db.Column(db.Integer, db.ForeignKey('producao.id'), nullable=False, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, primary_key=True)
    quantidade = db.Column(db.Float)