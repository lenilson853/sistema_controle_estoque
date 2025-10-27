# sistema_controle_estoque
Gestor de Estoque - Supermercado
Este é um sistema web completo para a gestão de estoque de um pequeno supermercado, desenvolvido em Python com o framework Flask.

O sistema permite o cadastro de mercadorias, controle de entrada e saída de estoque, geração de relatórios e automação de processos, como a exportação automática de dados para Excel.

Nota: Este projeto foi desenvolvido como um estudo de caso prático, combinando um backend robusto (Flask + SQLAlchemy) com um frontend responsivo (Bootstrap) e automação de tarefas (Pandas + Watchdog).

🖼️ Telas do Sistema
(Recomendação: Tire screenshots do seu app funcionando e coloque-os aqui. Isso deixa o README muito mais atraente!)

Exemplo de como adicionar uma imagem (você precisa subí-la para o GitHub primeiro): ![Tela Principal](link_para_sua_imagem.png)

Tela 1: Relatório de Estoque Atual * Tela 2: Cadastro de Produtos com Validação

Tela 3: Registro de Movimentos (Entrada/Saída)

✨ Funcionalidades Principais
CRUD de Produtos: Cadastro, leitura, atualização (implícita) e deleção (não implementada) de produtos.

Validação de EAN-13: O sistema valida se o código de barras inserido contém exatamente 13 dígitos numéricos.

Controle de Estoque: Registro manual de movimentos de Entrada (compras, recebimentos) e Saída (vendas, perdas).

Tratamento de Erros: O sistema exibe mensagens de erro amigáveis para o usuário (ex: "Produto já cadastrado") sem quebrar a aplicação.

Relatórios Detalhados:

Estoque Atual: Visão em tempo real de todos os produtos e suas quantidades.

Relatório de Saídas: Histórico de todos os produtos que saíram do estoque.

Relatório de Entradas: Histórico de todos os produtos que entraram no estoque.

Exportação Automática: A cada movimento de estoque, o relatório de "Estoque Atual" é automaticamente salvo em um arquivo Excel na pasta /data.

Automação de Entrada (2 formas):

API Endpoint: Um endpoint (/api/registrar_entrada) pronto para receber dados (JSON) de outro sistema (ex: um leitor de caixa).

Monitor de Pasta (Watcher): Um script (watcher.py) que monitora a pasta /watch_folder. Ao soltar um arquivo .xlsx ou .csv nela, o sistema lê o arquivo e registra as entradas automaticamente.

🚀 Tecnologias Utilizadas
Backend:

Python: Linguagem principal.

Flask: Micro-framework web para criar o servidor e as rotas (API).

Banco de Dados:

SQLite: Banco de dados leve e baseado em arquivo.

SQLAlchemy: ORM (Object-Relational Mapper) para interagir com o banco de dados usando Python.

Frontend:

HTML5: Estrutura das páginas.

Jinja2: Template engine do Flask para criar HTML dinâmico.

Bootstrap 5: Framework CSS para estilização rápida e responsiva.

Automação e Dados:

Pandas: Usado para criar e salvar os relatórios em arquivos Excel (.xlsx).

Watchdog: Biblioteca Python para monitorar eventos no sistema de arquivos (usada no watcher.py).

⚙️ Como Executar o Projeto
Siga os passos abaixo para rodar o sistema em sua máquina local.

1. Pré-requisitos
Python 3.8 ou superior.

pip (gerenciador de pacotes do Python).
