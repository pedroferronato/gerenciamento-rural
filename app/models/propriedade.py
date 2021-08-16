from app import db

class Propriedade(db.Model):
    __tablename__ = "propriedade"

    id = db.Column(db.Integer, primary_key=True)
    produtor_id = db.Column(db.Integer, db.ForeignKey('produtor.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
