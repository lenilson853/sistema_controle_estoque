from sqlalchemy import func, case
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.models import Produto, MovimentoEstoque
from app import db
from app import services
from sqlalchemy.exc import IntegrityError # Importação para capturar erro

# Define o Blueprint
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """ 
    Página Principal: Mostra um relatório resumido de 
    entradas, saídas e estoque atual por produto.
    """

    # 1. Define as colunas de soma que queremos calcular
    # Soma 'quantidade' SE o tipo for 'entrada', senão soma 0
    total_entradas = func.sum(
        case((MovimentoEstoque.tipo == 'entrada', MovimentoEstoque.quantidade), else_=0)
    ).label('total_entradas')
    
    # Soma 'quantidade' SE o tipo for 'saida', senão soma 0
    total_saidas = func.sum(
        case((MovimentoEstoque.tipo == 'saida', MovimentoEstoque.quantidade), else_=0)
    ).label('total_saidas')

    # 2. Monta a query principal
    # Pega todos os dados do Produto E as novas colunas calculadas
    relatorio_completo = db.session.query(
        Produto.id,
        Produto.nome,
        Produto.codigo_barras,
        Produto.preco_venda,
        Produto.estoque_atual,
        total_entradas,
        total_saidas
    ).outerjoin(MovimentoEstoque, Produto.id == MovimentoEstoque.produto_id # outerjoin para incluir produtos sem movimento
    ).group_by(Produto.id # Agrupa por produto
    ).order_by(Produto.nome # Ordena por nome
    ).all()

    # 3. Envia os resultados para o template
    # Note que mudamos 'produtos=produtos' para 'relatorio=relatorio_completo'
    return render_template('index.html', relatorio=relatorio_completo)


@bp.route('/produtos', methods=['GET', 'POST'])
def gerenciar_produtos():
    """ Página para Cadastrar novos produtos. """
    if request.method == 'POST':
        nome = request.form.get('nome')
        codigo = request.form.get('codigo_barras')
        preco = request.form.get('preco_venda')
        
        # --- VALIDAÇÃO DO CÓDIGO DE BARRAS ---
        if codigo: # Só valida se algo foi digitado
            if not codigo.isdigit():
                flash('Erro: O código de barras deve conter apenas números.', 'danger')
                return redirect(url_for('main.gerenciar_produtos'))
                
            if len(codigo) != 13:
                flash(f'Erro: O código de barras deve ter exatamente 13 dígitos. Você digitou {len(codigo)}.', 'danger')
                return redirect(url_for('main.gerenciar_produtos'))
        else:
            # Se o código for "", salva como None (Nulo) no DB
            codigo = None 
            
        try:
            # Tenta criar e salvar o novo produto
            novo_produto = Produto(
                nome=nome,
                codigo_barras=codigo,
                preco_venda=float(preco),
                estoque_atual=0
            )
            db.session.add(novo_produto)
            db.session.commit()
            
            flash(f'Produto {nome} cadastrado com sucesso!', 'success')
        
        except IntegrityError as e:
            # Captura erro de duplicidade
            db.session.rollback()
            # Verifica se o erro foi no nome ou no código de barras
            if 'produto.nome' in str(e.orig):
                flash(f'Erro: O produto com o nome "{nome}" já está cadastrado.', 'danger')
            elif 'produto.codigo_barras' in str(e.orig):
                flash(f'Erro: O código de barras "{codigo}" já está cadastrado em outro produto.', 'danger')
            else:
                flash(f'Erro de integridade no banco de dados: {e}', 'danger')
            
        except Exception as e:
            # Captura qualquer outro erro inesperado
            db.session.rollback()
            flash(f'Erro inesperado ao cadastrar: {e}', 'danger')
            
        return redirect(url_for('main.gerenciar_produtos'))
    
    # Se for um 'GET' (carregando a página)
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)


@bp.route('/movimento', methods=['GET', 'POST'])
def registrar_movimento_manual():
    """ Página para registrar Entradas e Saídas manualmente. """
    if request.method == 'POST':
        try:
            produto_id = request.form.get('produto_id')
            tipo = request.form.get('tipo') 
            quantidade = int(request.form.get('quantidade'))
            motivo = request.form.get('motivo')
            
            services.registrar_movimento(produto_id, tipo, quantidade, motivo)
            flash(f'Movimento ({tipo}) registrado com sucesso!', 'success')
            
        except Exception as e:
            flash(f'Erro ao registrar: {e}', 'danger')
            
        return redirect(url_for('main.registrar_movimento_manual'))

    produtos = Produto.query.all()
    return render_template('movimento.html', produtos=produtos)


@bp.route('/api/registrar_entrada', methods=['POST'])
def api_registrar_entrada():
    """ Endpoint para registro automático. """
    data = request.json
    produto = Produto.query.filter_by(codigo_barras=data.get('codigo_barras')).first()
    
    if not produto:
        return {"erro": "Produto não encontrado"}, 404
        
    try:
        services.registrar_movimento(
            produto_id=produto.id,
            tipo='entrada',
            quantidade=int(data.get('quantidade')),
            motivo=data.get('motivo', 'Entrada via API')
        )
        return {"sucesso": True, "estoque_atual": produto.estoque_atual}, 200
    except Exception as e:
        return {"erro": str(e)}, 400