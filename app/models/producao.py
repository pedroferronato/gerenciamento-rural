from app import db


class Producao(db.Model):
    __tablename__ = "producao"

    id = db.Column(db.Integer, primary_key=True)
    propriedade = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    produto = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    data = db.Column(db.Date(), nullable=False)
    data_coleta = db.Column(db.Date(), nullable=False)
