from app import db
from app.models.insumo import Insumo
from app.models.producao_insumo import ProducaoInsumo
from app.models.producao_produto import Coleta


class Producao(db.Model):
    __tablename__ = "producao"

    id = db.Column(db.Integer, primary_key=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float)
    quantidade_atual = db.Column(db.Float)
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

    
    def get_coletas(self):
        return Coleta.query.filter_by(producao_id=self.id).all()
        

    def quantidade_formatada(self):
        if self.quantidade.is_integer():
            return "{}".format(int(self.quantidade))
        return "{}".format(self.quantidade)
