from app import db
from models.livro import Livro

class Venda(db.Model):
    __tablename__ = 'venda'

    id = db.Column(db.Integer, primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=True)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    data_atualizacao = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamento com Livro
    livro = db.relationship('Livro', backref=db.backref('vendas', lazy=True))

    # Converter para dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'id_livro': self.id_livro,
            'valor': self.valor,
            'forma_pagamento': self.forma_pagamento,
            'data_criacao': self.data_criacao,
            'data_atualizacao': self.data_atualizacao,
            'livro': self.livro.to_dict() if self.livro else None  # Inclui os dados do livro, se houver
     
