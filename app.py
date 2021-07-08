from flask import (Flask, Blueprint, render_template, request, redirect, flash)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

user = 'kmvnfjma'
password = 'XG13yiZsTz5bajf9AibvbMl2P1gmcRJ7'
host = 'tuffi.db.elephantsql.com'
database = 'kmvnfjma'


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# nome da tabela: lista_produtos

class Lista_produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.Integer, nullable=False)
    quant_produto = db.Column(db.String(255), nullable=False)
    imagem_produto = db.Column(db.String(255), nullable=False)
    preco_produto = db.Column(db.Integer, nullable=False)
    descri_produto = db.Column(db.String(255), nullable=False)
    categoria_produto = db.Column(db.String(255), nullable=False)

    def __init__(self, nome_produto, quant_produto, imagem_produto, preco_produto, descri_produto, categoria_produto):

        self.nome_produto = nome_produto
        self.quant_produto = quant_produto
        self.imagem_produto = imagem_produto
        self.preco_produto = preco_produto
        self.descri_produto = descri_produto
        self.categoria_produto = categoria_produto

    @staticmethod
    def get_products():
        return Lista_produtos.query.all()

    @staticmethod
    def get_product_by_category(category):
        return Lista_produtos.query.filter_by(categoria_produto=category)

    @staticmethod
    def get_single_product(produto_id):
        return Lista_produtos.query.get(produto_id)

    def set_save(self):
        db.session.add(self)
        db.session.commit()

    def set_data(self, new_data):
        self.nome_produto = new_data.nome_produto
        self.quant_produto = new_data.quant_produto
        self.imagem_produto = new_data.imagem_produto
        self.preco_produto = new_data.preco_produto
        self.descri_produto = new_data.descri_produto
        self.categoria_produto = new_data.categoria_produto
        self.set_save()
    def del_data(self):
        db.session.delete(self)
        db.session.commit()

    def comprar(self, quantidade_vendida):
        self.quant_produto -= quantidade_vendida
        self.set_save()


@bp.route("/")
def main():
    peripheral = Lista_produtos.get_product_by_category('Periferico')
    hardware = Lista_produtos.get_product_by_category('Hardware')
    protector = Lista_produtos.get_product_by_category('Protector')
    print(peripheral)
    return render_template("index.html", path="/",  peripheral=peripheral,
                           hardware=hardware, protector=protector,
                           pageTitle="Pagina Inicial")


@bp.route("/produtos")
def ler():
    lista_produtos = Lista_produtos.get_products()
    return render_template("products_card.html", lista_produtos=lista_produtos, path="/produtos",pageTitle="Lista de produtos")


@bp.route("/criar-produto", methods=('GET', 'POST'))
def criar():
    id_atribuido = None

    if request.method == 'POST':
        form = request.form
        produto = Lista_produtos(
            form['nome_produto'],
            form['quant_produto'],
            form['imagem_produto'],
            form['preco_produto'],
            form['descri_produto'],
            form['categoria_produto'])
        produto.set_save()
        id_atribuido = produto.id

    return render_template('create-product.html', id_atribuido=id_atribuido, path="/criar-produto",pageTitle="Criar produto")


@bp.route('/atualizar/<produto_id>', methods=('GET', 'POST'))
def update(produto_id):
    condition_met = None
    produto = Lista_produtos.get_single_product(produto_id)

    if request.method == 'POST':
        form = request.form

        new_data = Lista_produtos(
            form['nome_produto'],
            form['quant_produto'],
            form['imagem_produto'],
            form['preco_produto'],
            form['descri_produto'],
            form['categoria_produto'])

        produto.set_data(new_data)

        condition_met = True

    return render_template('update.html', produto=produto, condition_met=condition_met)


@bp.route("/produtos/<produto_id>")
def ler_1(produto_id):
    produto = Lista_produtos.get_single_product(produto_id)
    return render_template("product.html", produto=produto, path="/produtos/<produto_id>",
                           pageTitle="Ver mais")


@bp.route('/deletar/<produto_id>')
def delete(produto_id):
    produto = Lista_produtos.get_single_product(produto_id)

    return render_template('delete.html', produto=produto)


@bp.route('/deletar/<produto_id>/confirmado')
def delete_confirmed(produto_id):
    condition_met = None
    produto = Lista_produtos.get_single_product(produto_id)

    if produto:
        produto.del_data()
        condition_met = True

    return render_template('delete.html', condition_met=condition_met)


@bp.route('/produtos/<produto_id>/comprar', methods=('GET', 'POST'))
def comprar(produto_id):
    condition_met = None
    produto = Lista_produtos.get_single_product(produto_id)

    if request.method == 'POST':
        form = request.form
        quantidade_comprada = int(form['quantity'])
        if quantidade_comprada <= produto.quant_produto:
            produto.comprar(quantidade_comprada)
            condition_met = True

    return render_template("product.html", produto=produto, path="/produtos/<produto_id>",
                           pageTitle="Ver mais", condition_met=condition_met)
    # return render_template('product.html',produto=produto, path="/produtos/<produto_id>/comprar",pageTitle = "Comprar produto")


app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
