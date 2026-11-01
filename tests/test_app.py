import sys
import os

# Adiciona a raiz do projeto ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, db, Animal

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_cadastrar_animal(client):
    response = client.post('/animais', data={
        'nome': 'Thor',
        'especie': 'Cachorro',
        'idade': '2 anos',
        'status_saude': 'Saudável',
        'historico': 'Resgatado sem ferimentos.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Thor' in response.data