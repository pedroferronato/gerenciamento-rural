from app import db


class Movimentador(db.Model):
    __tablename__ = "movimentador"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    contato = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
