import pandas as pd
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    preco = db.Column(db.Float, index=True)
    categoria = db.Column(db.String(256))

    def to_dict(self):
        return {
            'name': self.name,
            'preco': self.preco,
            'categoria': self.categoria
        }

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    cpf = db.Column(db.Integer, index=True)

    def to_dict(self):
        return {
            'name': self.name,
            'cpf': self.cpf
        }

db.create_all()


@app.route('/')
def index():
    return render_template('ajax_table.html', title='Ajax Table')

@app.route('/vendas')
def vendas():
    return render_template('vendas.html', title='Lista de vendas')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html', title='Lista de produtos')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', title='Lista de clientes')

@app.route('/nova_venda')
def nova_venda():
    df = pd.DataFrame(columns=['name', 'preco', 'categoria'])
    for produto in Produto.query:
        categoria = produto.categoria
        name = produto.name
        preco = produto.preco
        newrow = {'categoria': categoria, 'name': name, 'preco': preco}
        df = df.append(newrow, ignore_index=True)
    return render_template('nova_venda.html', title='Cadastro venda', df=df)

@app.route('/novo_produto', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        data = request.form.to_dict()
        produto = Produto(name=data['name'],
                          preco=data['price'],
                          categoria=data['categoria'])
        db.session.add(produto)
        db.session.commit()
    return render_template('novo_produto.html', title='Cadastro venda')

@app.route('/novo_cliente', methods=['GET', 'POST'])
def novo_cliente():
    # pdb.set_trace()
    if request.method == 'POST':
        data = request.form.to_dict()

        cliente = Cliente(name=data['name'],
                          cpf=data['cpf'])

        db.session.add(cliente)
        db.session.commit()
    return render_template('novo_cliente.html', title='Cadastro cliente')


@app.route('/api/data')
def data():
    return {'data': [user.to_dict() for user in User.query]}

@app.route('/api/produto')
def produto():
    return {'data': [produto.to_dict() for produto in Produto.query]}

@app.route('/api/cliente')
def cliente():
    return {'data': [cliente.to_dict() for cliente in Cliente.query]}

if __name__ == '__main__':
    app.run()
