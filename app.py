from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aumigos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.String(20), nullable=False)
    status_saude = db.Column(db.String(100), nullable=False)
    historico = db.Column(db.Text, nullable=True)

@app.route('/')
def index():
    animais = Animal.query.all()
    return render_template('index.html', animais=animais)

@app.route('/animais', methods=['POST'])
def cadastrar_animal():
    nome = request.form.get('nome')
    especie = request.form.get('especie')
    idade = request.form.get('idade')
    status_saude = request.form.get('status_saude')
    historico = request.form.get('historico')

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)