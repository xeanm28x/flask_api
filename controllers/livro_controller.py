from flask import Blueprint, request, jsonify
from models.livro import Livro
from db import db

livro_blueprint = Blueprint('livro', __name__)

# Listar todos os livros
@livro_blueprint.route('/', methods=['GET'])
def get_livros():
    livros = Livro.query.all()
    return jsonify(livros=[livro.to_dict() for livro in livros]), 200

# Criação de um novo livro com URL de capa
@livro_blueprint.route('/', methods=['POST'])
def create_livro():
    data = request.json
    if 'titulo' not in data or 'valor_unitario' not in data:
        return jsonify(message="Campos 'titulo' e 'valor_unitario' são obrigatórios."), 400

    livro = Livro(
        titulo=data['titulo'],
        autor=data.get('autor', 'Autor Desconhecido'),
        genero=data.get('genero'),
        numero_paginas=data.get('numero_paginas'),
        editora=data.get('editora'),
        edicao=data.get('edicao'),
        ano_publicacao=data.get('ano_publicacao'),
        valor_unitario=data['valor_unitario'],
        url_capa=data.get('url_capa')  # Adiciona o URL da capa, se presente
    )
    
    db.session.add(livro)
    db.session.commit()
    return jsonify(livro=livro.to_dict()), 201

# Obter um livro específico
@livro_blueprint.route('/<int:livro_id>', methods=['GET'])
def get_livro(livro_id):
    livro = Livro.query.get(livro_id)
    if not livro:
        return jsonify(message="Livro não encontrado."), 404
    return jsonify(livro=livro.to_dict()), 200

# Atualizar um livro específico
@livro_blueprint.route('/<int:livro_id>', methods=['PUT'])
def update_livro(livro_id):
    data = request.json
    livro = Livro.query.get(livro_id)
    if not livro:
        return jsonify(message="Livro não encontrado."), 404

    # Campos permitidos para atualização, incluindo 'valor_unitario'
    livro.titulo = data.get('titulo', livro.titulo)
    livro.autor = data.get('autor', livro.autor)
    livro.genero = data.get('genero', livro.genero)
    livro.numero_paginas = data.get('numero_paginas', livro.numero_paginas)
    livro.editora = data.get('editora', livro.editora)
    livro.edicao = data.get('edicao', livro.edicao)
    livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)
    livro.valor_unitario = data.get('valor_unitario', livro.valor_unitario)
    livro.url_capa = data.get('url_capa', livro.url_capa)
    
    # Salva as alterações no banco de dados
    db.session.commit()
    return jsonify(livro=livro.to_dict()), 200

# Deletar um livro específico
@livro_blueprint.route('/<int:livro_id>', methods=['DELETE'])
def delete_livro(livro_id):
    livro = Livro.query.get(livro_id)
    if not livro:
        return jsonify(message="Livro não encontrado."), 404
    db.session.delete(livro)
    db.session.commit()
    return jsonify(message="Livro deletado."), 200
