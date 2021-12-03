from app import db

class Propriedade(db.Model):
    __tablename__ = "propriedade"

    id = db.Column(db.Integer, primary_key=True)
    produtor_id = db.Column(db.Integer, db.ForeignKey('produtor.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(20))
    contato = db.Column(db.String(25))
    ativa = db.Column(db.Boolean(), default=True)
