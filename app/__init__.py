import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuração do Banco de Dados
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, '..', 'supermercado.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # --- ADICIONE ESTA LINHA ---
    # Pode ser qualquer texto, mas deve ser secreto
    app.config['SECRET_KEY'] = 'minha-chave-secreta-ninguem-sabe-123'
    # ---------------------------
    
    db.init_app(app)
    
    from app import routes
    app.register_blueprint(routes.bp)

    from app import models

    with app.app_context():
        db.create_all()
        
    return app