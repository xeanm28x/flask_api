from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from controllers.livro_controller import livro_blueprint
from controllers.venda_controller import venda_blueprint

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskapi.db'  # Armazena o banco no arquivo flaskapi.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Blueprints para as rotas de livros e vendas
app.register_blueprint(livro_blueprint, url_prefix='/livros')
app.register_blueprint(venda_blueprint, url_prefix='/vendas')

@app.route('/')
def home():
    return jsonify(message="Hello World! (Teste) =)"), 200

if __name__ == '__main__':
    # Certifica-se de que o banco de dados e as tabelas estão criados
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
