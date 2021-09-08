from app import db

class MovimentacaoFinanceira(db.Model):
    __tablename__ = "movimentacao_financeira"

    id = db.Column(db.Integer, primary_key=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    data = db.Column(db.Date(), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
