from app import db


class MovimetacaoFinanceiraItem(db.Model):
    __tablename__ = "movimentacao_financeira_item"

    movimentacao_financeira_id = db.Column(db.Integer, db.ForeignKey('movimentacao_financeira.id'), nullable=False, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, primary_key=True)
    movimentador_id = db.Column(db.Integer, db.ForeignKey('movimentador.id'), nullable=False, primary_key=True)
    quantidade = db.Column(db.Float, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
