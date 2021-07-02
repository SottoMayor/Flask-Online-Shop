from flask import (Flask, Blueprint, render_template)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

user = 'kmvnfjma'
password = 'XG13yiZsTz5bajf9AibvbMl2P1gmcRJ7'
host = 'tuffi.db.elephantsql.com'
database = 'kmvnfjma'


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@' + \
    f'{host}/{database}'
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

    def get_products():
        return Lista_produtos.query.all()


@bp.route("/")
def main():
    return render_template("header.html")


@bp.route("/produtos")
def ler():
    lista_produtos = Lista_produtos.get_products()
    return render_template("products.html", lista_produtos=lista_produtos)


@bp.route("/criar-produto")
def criar():
    return render_template("create-product.html")


app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
