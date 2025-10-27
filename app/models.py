from app import db # 'db' será criado no __init__.py
from datetime import datetime

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    codigo_barras = db.Column(db.String(50), unique=True, index=True)
    preco_venda = db.Column(db.Float, nullable=False)
    estoque_atual = db.Column(db.Integer, default=0)
    
    # Relação: Um produto pode ter vários movimentos de estoque
    movimentos = db.relationship('MovimentoEstoque', backref='produto', lazy=True)

class MovimentoEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False) # 'entrada' ou 'saida'
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.String(200)) # Ex: "Venda", "Recebimento Fornecedor", "Ajuste"
    
    # Chave estrangeira para linkar ao produto
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)