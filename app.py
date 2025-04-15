from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surfskate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mensagem = db.Column(db.Text)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    data = db.Column(db.String(20))
    descricao = db.Column(db.Text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/eventos')
def eventos():
    eventos = Evento.query.all()
    return render_template('eventos.html', eventos=eventos)

@app.route('/contato', methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        novo_contato = Contato(nome=nome, email=email, mensagem=mensagem)
        db.session.add(novo_contato)
        db.session.commit()
        return render_template("contato.html", success="Mensagem enviada com sucesso!")
    return render_template("contato.html")

@app.route('/cadastro-evento', methods=["GET", "POST"])
def cadastro_evento():
    if request.method == 'POST':
        titulo = request.form['titulo']
        data = request.form['data']
        descricao = request.form['descricao']
        novo_evento = Evento(titulo=titulo, data=data, descricao=descricao)
        db.session.add(novo_evento)
        db.session.commit()
        return render_template('cadastro_evento.html', success="Evento cadastrado com sucesso!")
    return render_template('cadastro_evento.html')

if __name__ == '__main__':
    app.run(debug=True)