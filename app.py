from flask import (Flask, Blueprint, render_template, request)
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

    def set_save(self):
        db.session.add(self)
        db.session.commit()

    def set_data(self, new_data):
        self.nome_produto = new_data.nome_produto
        self.quant_produto = new_data.quant_produto
        self.imagem_produto = new_data.imagem_produto
        self.set_save()
    
    def del_data(self):
        db.session.delete(self)
        db.session.commit()


@bp.route("/")
def main():
    return render_template("index.html",path="/",pageTitle = "Pagina Inicial")


@bp.route("/produtos")
def ler():
    lista_produtos = Lista_produtos.get_products()
    return render_template("products_card.html", lista_produtos=lista_produtos,path="/produtos",
    pageTitle = "Lista de produtos")


@bp.route("/criar-produto",methods=('GET','POST'))
def criar():
    id_atribuido = None

    if request.method == 'POST':
        form = request.form
        produto = Lista_produtos(
            form['nome_produto'],
            form['quant_produto'],
            form['imagem_produto'])
        produto.set_save()
        id_atribuido = produto.id

    return render_template('create-product.html', id_atribuido=id_atribuido, path="/criar-produto",
    pageTitle = "Criar produto")

@bp.route('/atualizar/<produto_id>',methods=('GET','POST'))
def update(produto_id):
    condition_met = None
    produto = Lista_produtos.get_single_product(produto_id)

    if request.method == 'POST':
        form=request.form
    
        new_data = Lista_produtos(form['nome_produto'],form['quant_produto'],form['imagem_produto'])

        produto.set_data(new_data)

        condition_met = True

    return render_template('update.html',produto=produto,condition_met=condition_met)

@bp.route("/produtos/<produto_id>")
def ler_1(produto_id):
    produto = Lista_produtos.get_single_product(produto_id)
    return render_template("product.html",produto=produto,path="/produtos/<produto_id>",
    pageTitle = "Produto {{produto.nome}}")

@bp.route('/deletar/<produto_id>')
def delete(produto_id):
    produto = Lista_produtos.get_single_product(produto_id)

    return render_template('delete.html',produto=produto)

@bp.route('/deletar/<produto_id>/confirmado')
def delete_confirmed(produto_id):
    condition_met = None
    produto = Lista_produtos.get_single_product(produto_id)

    if produto:
        produto.del_data()
        condition_met = True

    return render_template('delete.html',condition_met=condition_met)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
