from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do Banco de Dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'aumigos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Dados para os Animais Resgatados
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.String(20), nullable=True)
    status_saude = db.Column(db.String(100), nullable=False)
    historico = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Animal {self.nome}>'

# Rota Principal: Listagem de Animais
@app.route('/')
def index():
    animais = Animal.query.all()
    return render_template('index.html', animais=animais)

# Rota de Cadastro de Novos Animais
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    especie = request.form.get('especie')
    idade = request.form.get('idade')
    status_saude = request.form.get('status_saude')
    historico = request.form.get('historico')

    if nome and especie:
        novo_animal = Animal(
            nome=nome,
            especie=especie,
            idade=idade,
            status_saude=status_saude,
            historico=historico
        )
        db.session.add(novo_animal)
        db.session.commit()

    return redirect(url_for('index'))

# Bloco de inicialização e execução local/servidor
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=10000, debug=True)
else:
    # Garante que as tabelas são criadas também quando executado via Gunicorn no Render
    with app.app_context():
        db.create_all()