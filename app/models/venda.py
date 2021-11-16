from app import db
from app.models.movimentador import Movimentador
from app.models.produto import Produto


class Venda(db.Model):
    __tablename__ = "venda"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    data = db.Column(db.Date(), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False, primary_key=True)
    movimentador_id = db.Column(db.Integer, db.ForeignKey('movimentador.id'), nullable=False, primary_key=True)
    quantidade = db.Column(db.Float, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)


    def get_cliente(self):
        return Movimentador.query.filter_by(id=self.movimentador_id).first()


    def get_produto(self):
        return Produto.query.filter_by(id=self.produto_id).first()


    def valor_final_formatado(self):
        return 'R$ {:.2f}'.format(self.valor_total)


    def valor_unitario_formatado(self):
        return 'R$ {:.2f}'.format(self.valor_unitario)


    def quantidade_formatada(self):
        if self.quantidade.is_integer():
            return "{} {}".format(int(self.quantidade), self.get_produto().unidade_medida)
        return "{} {}".format(self.quantidade, self.get_produto().unidade_medida)    
