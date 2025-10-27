import pandas as pd
import os
from app import db
from app.models import Produto, MovimentoEstoque

# Define o caminho da pasta de dados
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def registrar_movimento(produto_id, tipo, quantidade, motivo):
    """
    Função central para registrar entradas/saídas e ATUALIZAR o estoque do produto.
    """
    produto = Produto.query.get(produto_id)
    if not produto:
        raise Exception("Produto não encontrado")

    # Cria o registro do movimento
    movimento = MovimentoEstoque(
        produto=produto,
        tipo=tipo,
        quantidade=quantidade,
        motivo=motivo
    )
    
    # Atualiza o estoque atual no cadastro do produto
    if tipo == 'entrada':
        produto.estoque_atual += quantidade
    elif tipo == 'saida':
        if produto.estoque_atual < quantidade:
            raise Exception(f"Estoque insuficiente para {produto.nome}")
        produto.estoque_atual -= quantidade
    
    db.session.add(movimento)
    db.session.add(produto) # Adiciona o produto para atualizar o estoque
    db.session.commit()
    
    # Após cada movimento, atualiza o Excel (REQUISITO)
    exportar_relatorio_estoque()
    
    return True

def exportar_relatorio_estoque():
    """
    Exporta o status atual do estoque para um arquivo Excel na pasta /data.
    """
    try:
        # Pega todos os produtos
        produtos = Produto.query.all()
        data = [{
            'id': p.id,
            'nome': p.nome,
            'codigo_barras': p.codigo_barras,
            'preco_venda': p.preco_venda,
            'estoque_atual': p.estoque_atual
        } for p in produtos]
        
        df = pd.DataFrame(data)
        
        # Caminho do arquivo
        filepath = os.path.join(DATA_DIR, 'relatorio_estoque_atual.xlsx')
        
        # Salva em Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        print(f"Relatório de estoque salvo em {filepath}")
        
    except Exception as e:
        print(f"Erro ao exportar Excel: {e}")