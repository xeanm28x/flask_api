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

    # Validação dos campos obrigatórios
    if 'id_livro' not in data or 'quantidade' not in data:
        return jsonify(message="O livro e a quantidade são obrigatórios."), 400

    # Verifica se o livro existe
    livro = Livro.query.get(data['id_livro'])
    if not livro:
        return jsonify(message="Livro não encontrado."), 404

    # Cria a venda com o livro e quantidade especificados
    venda = Venda(
        livro_id=data['id_livro'],
        quantidade=data['quantidade'],
        livro=livro  # Passa a instância do livro para calcular o valor
    )
    venda.calcular_valor_total()  # Usa a função do modelo para calcular o valor total

    # Gera o QR Code
    qr_code_response = gerar_qr_code(data['id_livro'], venda.valor_total)
    if qr_code_response and 'qr_code_base64' in qr_code_response:
        qr_code_url = qr_code_response['qr_code_base64']
    else:
        return jsonify(message="Erro ao gerar QR Code."), 500

    # Salva a venda no banco de dados
    db.session.add(venda)
    db.session.commit()

    # Retorna a resposta com a venda e o QR Code
    response_data = {
        'message': 'Venda efetuada com sucesso!',
        'venda': venda.to_dict(),
        'qr_code_url': qr_code_url
    }

    return jsonify(response_data), 201

# Rota para obter uma venda específica
@venda_blueprint.route('/<int:venda_id>', methods=['GET'])
def get_venda(venda_id):
    venda = Venda.query.get(venda_id)
    if not venda:
        return jsonify(message="Venda não encontrada."), 404
    return jsonify(venda=venda.to_dict()), 200
