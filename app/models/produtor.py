from app import db
from app.models.propriedade import Propriedade
from flask_login import UserMixin


class Produtor(db.Model, UserMixin):
    __tablename__ = "produtor"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    login = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(150), nullable=False)
    contato = db.Column(db.String(25))


    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return self.id

    
    def get_propriedade(self):
        return Propriedade.query.filter(
            Propriedade.ativa == True,
            Propriedade.produtor_id == self.id
        ).first()
