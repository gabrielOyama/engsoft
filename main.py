import pandas as pd
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Venda(db.Model):
    id_venda = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), index=True)
    vendedor = db.Column(db.String(100), index=True)
    data = db.Column(db.DateTime)
    valor = db.Column(db.Float)
    produtos = db.Column(db.String(500))

    def to_dict(self):
        return {
            'cliente': self.cliente,
            'vendedor': self.vendedor,
            'data': self.data,
            'valor': self.valor,
            'produtos': self.produtos
        }

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    preco = db.Column(db.Float, index=True)
    categoria = db.Column(db.String(256))
    aVenda = db.Column(db.Boolean, index=True)
    def to_dict(self):
        return {
            'name': self.name,
            'preco': self.preco,
            'categoria': self.categoria,
            'aVenda': self.aVenda
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

class Vendedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    cpf = db.Column(db.Integer, index=True)
    email = db.Column(db.String(64), index=True)
    isActive = db.Column(db.Boolean, index=True)

    def to_dict(self):
        return {
            'name': self.name,
            'cpf': self.cpf,
            'email': self.email,
            'isActive': self.isActive
        }

db.create_all()


@app.route('/')
@app.route('/vendas')
def vendas():
    return render_template('vendas.html', title='Lista de vendas')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html', title='Lista de produtos')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', title='Lista de clientes')


@app.route('/vendedores')
def vendedores():
    return render_template('vendedores.html', title='Cadastro venda')


@app.route('/nova_venda', methods=['GET', 'POST'])
def nova_venda():
    if request.method == 'POST':
        data = request.form.to_dict()

        venda = Venda(cliente=data['cliente'],
                      vendedor=data['vendedor'],
                      produtos=data['compras'],
                      valor=data['valorFinal'],
                      data=datetime.today())
        db.session.add(venda)
        ok = db.session.commit()
        return render_template('vendas.html', title='Lista de vendas')
    else:
        df_cliente = pd.DataFrame(columns=['name'])
        for cliente in Cliente.query:
            name = cliente.name
            newrow = {'name': name}
            df_cliente = df_cliente.append(newrow, ignore_index=True)

        df_vendedor = pd.DataFrame(columns=['name'])
        for vendedor in Vendedor.query:
            if vendedor.isActive:
                name = vendedor.name
                newrow = {'name': name}
                df_vendedor = df_vendedor.append(newrow, ignore_index=True)

        df_produto = pd.DataFrame(columns=['name', 'preco', 'categoria', 'nomeP'])
        for produto in Produto.query:
            if produto.aVenda:
                categoria = produto.categoria
                name = produto.name
                preco = produto.preco
                nomeP = produto.name.replace(' ', '_') + '_' + str(produto.preco)
                newrow = {'categoria': categoria, 'name': name, 'preco': preco, 'nomeP': nomeP}
                df_produto = df_produto.append(newrow, ignore_index=True)
        return render_template('nova_venda.html', title='Cadastro venda', df_cliente=df_cliente, df_produto= df_produto, df_vendedor=df_vendedor)

@app.route('/novo_produto', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        data = request.form.to_dict()
        produto = Produto(name=data['name'],
                          preco=data['price'].replace(',','.'),
                          categoria=data['categoria'],
                          aVenda= True)
        db.session.add(produto)
        db.session.commit()
    return render_template('novo_produto.html', title='Cadastro venda')

@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def novo_cliente():
    # pdb.set_trace()
    if request.method == 'POST':
        data = request.form.to_dict()

        cliente = Cliente(name=data['name'],
                          cpf=data['cpf'])

        db.session.add(cliente)
        db.session.commit()
    return render_template('novo_cliente.html', title='Cadastro cliente')

@app.route('/novo_vendedor', methods=['GET', 'POST'])
def novo_vendedor():
    # pdb.set_trace()
    if request.method == 'POST':
        data = request.form.to_dict()

        vendedor = Vendedor(name=data['name'],
                          cpf=data['cpf'],
                          email=data['email'],
                          isActive= data['isActive'] == 'true')

        db.session.add(vendedor)
        db.session.commit()
    return render_template('novo_vendedor.html', title='Cadastro vendedor')

@app.route('/update_vendedor', methods=['GET', 'POST'])
def update_vendedor():
    # pdb.set_trace()
    if request.method == 'POST':
        data = request.form.to_dict()

        db.session.query(Vendedor).filter(Vendedor.cpf == data['cpf']).update({'isActive': data['isActive'] == 'true'})
        db.session.commit()


    return render_template('update_vendedor.html', title='Cadastro vendedor')

@app.route('/update_produto', methods=['GET', 'POST'])
def update_produto():
    # pdb.set_trace()
    if request.method == 'POST':
        data = request.form.to_dict()

        db.session.query(Produto).filter(Produto.name == data['name']).update({'aVenda': data['aVenda'] == 'true'})
        if len(data['price']) > 0:
            db.session.query(Produto).filter(Produto.name == data['name']).update({'preco': data['price']})
        db.session.commit()


    return render_template('update_produto.html', title='Cadastro vendedor')

@app.route('/api/data')
def data():
    return {'data': [vendas.to_dict() for vendas in Venda.query]}

@app.route('/api/produto')
def produto():
    return {'data': [produto.to_dict() for produto in Produto.query]}

@app.route('/api/cliente')
def cliente():
    return {'data': [cliente.to_dict() for cliente in Cliente.query]}

@app.route('/api/vendedor')
def vendedor():
    return {'data': [vendedor.to_dict() for vendedor in Vendedor.query]}

if __name__ == '__main__':
    app.run()
