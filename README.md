# 🐾 Sistema Integrado Aumigos (MVP Flask)

Plataforma web desenvolvida em Python (Flask) com o objetivo de apoiar a gestão operacional de resgates de animais, o controle clínico e a triagem transparente de suprimentos comunitários. O projeto está alinhado com o **ODS 15 (Vida Terrestre)**, promovendo a conservação, o manejo sustentável da fauna e o apoio a iniciativas de proteção animal.

---

## 🚀 Tecnologias Utilizadas

O projeto foi construído utilizando uma stack tecnológica moderna, leve e robusta:
* **Linguagem:** Python 3.10+
* **Framework Web:** Flask
* **Mapeamento Objeto-Relacional (ORM):** Flask-SQLAlchemy
* **Base de Dados:** SQLite (`aumigos.db`)
* **Interface / Estilização:** HTML5, Jinja2 Templates e Bootstrap 5
* **Servidor de Produção:** Gunicorn
* **Controlo de Versão e CI:** Git, GitHub e GitHub Actions

---

## 📂 Estrutura do Projeto

```text
projeto-aumigos/
│
├── .github/workflows/     # Automação de testes e CI (GitHub Actions)
├── instance/              # Ficheiros de base de dados SQLite (aumigos.db)
├── templates/             # Ficheiros HTML com herança de layout
│   ├── base.html          # Layout base com barra de navegação responsiva
│   ├── index.html         # Dashboard principal com indicadores
│   ├── animais.html       # Gestão, registo e exclusão de animais
│   ├── triagem.html       # Controle e associação de suprimentos por animal
│   └── relatorios.html    # Relatórios de impacto e alinhamento ODS 15
├── tests/                 # Testes automatizados do sistema
├── app.py                 # Ficheiro principal da aplicação Flask e rotas
├── requirements.txt       # Dependências do projeto
├── Procfile               # Configuração para deploy em nuvem (Render)
└── README.md              # Documentação oficial do repositório