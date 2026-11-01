from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aumigos-secret-key-2026'

# Configuração da base de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'aumigos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Dados: Animais Resgatados
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.String(50), nullable=False)
    status_saude = db.Column(db.String(200), nullable=False)
    # Relação com os suprimentos
    suprimentos = db.relationship('Suprimento', backref='animal_destinado', lazy=True, cascade='all, delete-orphan')

# Modelo de Dados: Suprimentos / Triagem (Com vínculo ao animal)
class Suprimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150), nullable=False)
    quantidade_kg = db.Column(db.Float, nullable=False)
    data_registro = db.Column(db.String(50), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)

with app.app_context():
    db.create_all()

# Rotas de Navegação (Abas do Sistema)
@app.route('/')
def index():
    total_animais = Animal.query.count()
    total_suprimentos = db.session.query(db.func.sum(Suprimento.quantidade_kg)).scalar() or 0
    return render_template('index.html', total_animais=total_animais, total_suprimentos=total_suprimentos)

@app.route('/animais', methods=['GET', 'POST'])
def animais():
    if request.method == 'POST':
        nome = request.form.get('nome')
        especie = request.form.get('especie')
        idade = request.form.get('idade')
        status_saude = request.form.get('status_saude')
        
        if nome and especie:
            novo_animal = Animal(nome=nome, especie=especie, idade=idade, status_saude=status_saude)
            db.session.add(novo_animal)
            db.session.commit()
            flash('Animal registado com sucesso!', 'success')
        return redirect(url_for('animais'))
    
    lista_animais = Animal.query.all()
    return render_template('animais.html', animais=lista_animais)

@app.route('/deletar_animal/<int:id>', methods=['POST'])
def deletar_animal(id):
    animal = Animal.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    flash('Registo do animal e os seus suprimentos associados foram removidos!', 'warning')
    return redirect(url_for('animais'))

@app.route('/triagem', methods=['GET', 'POST'])
def triagem():
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        qtd = float(request.form.get('quantidade_kg') or 0)
        data = request.form.get('data_registro') # Formato AAAA-MM-DD vindo do input date
        animal_id = request.form.get('animal_id')
        
        if descricao and qtd > 0 and animal_id and data:
            # Converte a data para o padrão brasileiro (DD/MM/AAAA)
            partes = data.split('-')
            data_formatada = f"{partes[2]}/{partes[1]}/{partes[0]}" if len(partes) == 3 else data
            
            novo_sup = Suprimento(descricao=descricao, quantidade_kg=qtd, data_registro=data_formatada, animal_id=int(animal_id))
            db.session.add(novo_sup)
            db.session.commit()
            flash('Lote de suprimentos associado ao animal com sucesso!', 'success')
        return redirect(url_for('triagem'))
        
    lista_suprimentos = Suprimento.query.all()
    lista_animais = Animal.query.all()
    total_kg = sum(s.quantidade_kg for s in lista_suprimentos)
    return render_template('triagem.html', suprimentos=lista_suprimentos, animais=lista_animais, total_kg=total_kg)

@app.route('/deletar_suprimento/<int:id>', methods=['POST'])
def deletar_suprimento(id):
    suprimento = Suprimento.query.get_or_404(id)
    db.session.delete(suprimento)
    db.session.commit()
    flash('Registo de suprimento removido com sucesso!', 'warning')
    return redirect(url_for('triagem'))

@app.route('/relatorios')
def relatorios():
    total_animais = Animal.query.count()
    total_suprimentos = db.session.query(db.func.sum(Suprimento.quantidade_kg)).scalar() or 0
    return render_template('relatorios.html', total_animais=total_animais, total_suprimentos=total_suprimentos)

if __name__ == '__main__':
    app.run(debug=True)