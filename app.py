from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surfskate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_secreta_para_teste' 

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

# Rotas públicas
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

# Autenticação simples
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form['senha']
        if senha == '1234':  # Altere aqui sua senha
            session['logado'] = True
            return redirect(url_for('listar_contatos'))
        else:
            return render_template('login.html', erro='Senha incorreta')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

# Rota protegida
@app.route('/contatos')
def listar_contatos():
    if not session.get('logado'):
        return redirect(url_for('login'))
    contatos = Contato.query.all()
    return render_template('listar_contatos.html', contatos=contatos)

if __name__ == '__main__':
    app.run(debug=True)