from app import db

class Livro(db.Model):
    __tablename__ = 'livro'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(50), default='Autor Desconhecido')
    genero = db.Column(db.String(50), nullable=True)
    numero_paginas = db.Column(db.Integer, nullable=True)
    editora = db.Column(db.String(50), nullable=True)
    edicao = db.Column(db.String(20), nullable=True)
    ano_publicacao = db.Column(db.Integer, nullable=True)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    data_atualizacao = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Converter para dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'genero': self.genero,
            'numero_paginas': self.numero_paginas,
            'editora': self.editora,
            'edicao': self.edicao,
            'ano_publicacao': self.ano_publicacao,
            'data_criacao': self.data_criacao,
            'data_atualizacao': self.data_atualizacao
        }
