from flask import Flask, render_template
from flask_cors import CORS
from db import db
from controllers.livro_controller import livro_blueprint
from controllers.venda_controller import venda_blueprint

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(livro_blueprint, url_prefix='/livros')
app.register_blueprint(venda_blueprint, url_prefix='/vendas')

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
