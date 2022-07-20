from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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
db.create_all()


@app.route('/')
def index():
    return render_template('ajax_table.html', title='Ajax Table')

@app.route('/vendas')
def vendas():
    return render_template('vendas.html', title='Cadastro venda')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html', title='Cadastro venda')

@app.route('/nova_venda')
def nova_venda():
    return render_template('nova_venda.html', title='Cadastro venda')

@app.route('/novo_produto')
def novo_produto():
    return render_template('novo_produto.html', title='Cadastro venda')


@app.route('/api/data')
def data():
    return {'data': [user.to_dict() for user in User.query]}

@app.route('/api/produto')
def produto():
    return {'data': [produto.to_dict() for produto in Produto.query]}

if __name__ == '__main__':
    app.run()
