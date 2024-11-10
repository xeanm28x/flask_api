from flask import Blueprint, request, jsonify
from models.venda import Venda
from models.livro import Livro
from db import db
import requests

venda_blueprint = Blueprint('venda', __name__)

# Função para gerar QR Code chamando o micro serviço
def gerar_qr_code(id_livro, valor):
    try:
        response = requests.post(
            'http://localhost:5000/gerar_qr_code',  # URL do micro serviço
            json={'id_livro': id_livro, 'valor': valor},
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Lança um erro se o status não for 200
        return response.json()  # Retorna a resposta em JSON
    except requests.exceptions.RequestException as e:
        print(f"Erro ao gerar QR Code: {e}")
        return None

# Rota para criar uma nova venda
@venda_blueprint.route('/', methods=['POST'])
def create_venda():
    data = request.json

    # Validação dos campos
    if 'id_livro' not in data or 'valor' not in data or 'forma_pagamento' not in data:
        return jsonify(message="Campos 'id_livro', 'valor' e 'forma_pagamento' são obrigatórios."), 400
    if data['forma_pagamento'] not in ['pix', 'credito']:
        return jsonify(message="A forma de pagamento deve ser 'pix' ou 'credito'."), 400

    # Verifica se o livro existe
    livro = Livro.query.get(data['id_livro'])
    if not livro:
        return jsonify(message="Livro não encontrado."), 404

    # Gera o QR Code se a forma de pagamento for "pix"
    qr_code_url = None
    if data['forma_pagamento'] == 'pix':
        qr_code_response = gerar_qr_code(data['id_livro'], data['valor'])
        if qr_code_response and 'qr_code_base64' in qr_code_response:
            qr_code_url = qr_code_response['qr_code_base64']
        else:
            return jsonify(message="Erro ao gerar QR Code."), 500

    # Cria a venda
    venda = Venda(
        id_livro=data['id_livro'],
        valor=data['valor'],
        forma_pagamento=data['forma_pagamento']
    )
    db.session.add(venda)
    db.session.commit()

    # Retorna a resposta com a venda e o QR Code, se aplicável
    response_data = {
        'message': 'Venda efetuada com sucesso!',
        'venda': venda.to_dict()
    }
    if qr_code_url:
        response_data['qr_code_url'] = qr_code_url

    return jsonify(response_data), 201

# Rota para obter uma venda específica
@venda_blueprint.route('/<int:venda_id>', methods=['GET'])
def get_venda(venda_id):
    venda = Venda.query.get(venda_id)
    if not venda:
        return jsonify(message="Venda não encontrada."), 404
    return jsonify(venda=venda.to_dict()), 200
