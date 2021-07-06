from flask import (Flask, Blueprint, render_template)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

# Dados para conexão com DB
user = 'kmvnfjma'
password = 'XG13yiZsTz5bajf9AibvbMl2P1gmcRJ7'
host = 'tuffi.db.elephantsql.com'
database = 'kmvnfjma'

# Conectando DB
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:' + \
    f'{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# nome da tabela: lista_produtos
class Lista_produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.Integer, nullable=False)
    quant_produto = db.Column(db.String(255), nullable=False)
    imagem_produto = db.Column(db.String(255), nullable=False)

    def __init__(self, nome_produto, quant_produto, imagem_produto):

        self.nome_produto = nome_produto
        self.quant_produto = quant_produto
        self.imagem_produto = imagem_produto

    @staticmethod
    def get_products():
        return Lista_produtos.query.all()

    @staticmethod
    def get_single_product(produto_id):
        return Lista_produtos.query.get(produto_id)


@bp.route("/")
def main():
    return render_template("index.html", pageTitle='Home', path='/')


@bp.route("/produtos")
def ler():
    lista_produtos = Lista_produtos.get_products()
    return render_template("products_card.html", lista_produtos=lista_produtos,
                           pageTitle='Todos os Produtos',
                           path='/produtos')


@bp.route("/criar-produto")
def criar():
    return render_template("create-product.html", path='/criar-produto')


@bp.route("/produtos/<produto_id>")
def ler_1(produto_id):
    produto = Lista_produtos.get_single_product(produto_id)
    print(produto)
    return render_template("product.html", produto=produto, path='/produtos',
                           pageTitle='Detalhes Sobre ' + produto.nome_produto)


app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
