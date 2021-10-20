from app import db


class Producao(db.Model):
    __tablename__ = "producao"

    id = db.Column(db.Integer, primary_key=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    ativa = db.Column(db.Boolean(), default=True)
    data = db.Column(db.Date(), nullable=False)
    data_coleta = db.Column(db.Date())
