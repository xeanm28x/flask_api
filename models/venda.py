from db import db

class Venda(db.Model):
    __tablename__ = 'venda'
    
    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=db.func.current_timestamp())

    livro = db.relationship('Livro', backref='vendas')

    def calcular_valor_total(self):
        if self.livro:
            # Arredonda o valor total para duas casas decimais
            self.valor_total = round(self.livro.valor_unitario * self.quantidade, 2)

    def to_dict(self):
        return {
            'id': self.id,
            'livro_id': self.livro_id,
            'quantidade': self.quantidade,
            'valor_total': self.valor_total,
            'data_venda': self.data_venda
        }
