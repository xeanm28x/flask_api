from flask import Flask, jsonify
from db import db
from controllers.livro_controller import livro_blueprint
from controllers.venda_controller import venda_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(livro_blueprint, url_prefix='/livros')
app.register_blueprint(venda_blueprint, url_prefix='/vendas')

@app.route('/')
def home():
    return jsonify(message="Hello World! (Teste) =)"), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
