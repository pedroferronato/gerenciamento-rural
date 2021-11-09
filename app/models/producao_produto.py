from app import db


class Coleta(db.Model):
    __tablename__ = "coleta"

    id = db.Column(db.Integer, primary_key=True)
    data_coleta = db.Column(db.Date(), nullable=False)
    quantidade = db.Column(db.Float)
    unidade_especifica = db.Column(db.String(50))
    producao_id = db.Column(db.Integer, db.ForeignKey('producao.id'), nullable=False)


    def quantidade_formatada(self):
        if self.quantidade.is_integer():
            return "{} {}".format(int(self.quantidade), self.unidade_especifica)
        return "{} {}".format(self.quantidade, self.unidade_especifica)
