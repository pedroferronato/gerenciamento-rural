from app import db


class Movimentador(db.Model):
    __tablename__ = "movimentador"

    id = db.Column(db.Integer, primary_key=True)
    produtor_id = db.Column(db.Integer, db.ForeignKey('produtor.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    contato = db.Column(db.String(100))
    endereco = db.Column(db.String(200))
    tipo = db.Column(db.String(20), nullable=False)
