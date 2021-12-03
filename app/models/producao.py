from app import db
from app.models.insumo import Insumo
from app.models.producao_insumo import ProducaoInsumo
from app.models.producao_produto import Coleta
from app.models.produto import Produto


class Producao(db.Model):
    __tablename__ = "producao"

    id = db.Column(db.Integer, primary_key=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    quantidade_atual = db.Column(db.Float)
    produto_esperado = db.Column(db.String(200))
    ativa = db.Column(db.Boolean(), default=True)
    data = db.Column(db.Date(), nullable=False)
    data_coleta = db.Column(db.Date())


    def get_insumo_base(self):
        filtros = [
            ProducaoInsumo.base == True,
            ProducaoInsumo.producao_id == self.id
        ]
        producao_insumo = ProducaoInsumo.query.filter(*filtros).first()
        return Insumo.query.filter_by(id=producao_insumo.insumo_id).first()


    def get_insumos_adicionados(self):
        filtros = [
            ProducaoInsumo.base == False,
            ProducaoInsumo.producao_id == self.id
        ]
        return ProducaoInsumo.query.filter(*filtros).all()


    def get_custos(self):
        despesas_producao = ProducaoInsumo.query.filter_by(producao_id=self.id).all()

        if len(despesas_producao) <= 0:
            return 0
        
        despesa_final = 0

        for despesa in despesas_producao:
            despesa_final += despesa.quantidade_aplicada * despesa.get_insumo_relacionado().valor_unitario

        return despesa_final

    
    def get_coletas(self):
        return Coleta.query.filter_by(producao_id=self.id).all()
        

    def quantidade_formatada(self):
        if self.quantidade.is_integer():
            return "{}".format(int(self.quantidade))
        return "{}".format(self.quantidade)


    def quantidade_atual_formatada(self):
        if self.quantidade_atual.is_integer():
            return "{}".format(int(self.quantidade_atual))
        return "{}".format(self.quantidade_atual)
