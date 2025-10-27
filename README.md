# 🧮 Gestor de Estoque - Supermercado

**Sistema web completo** para a gestão de estoque de um pequeno supermercado, desenvolvido em **Python (Flask)**.  
O sistema permite o **cadastro de mercadorias**, **controle de entrada e saída de estoque**, **geração de relatórios** e **automação de processos**, como a exportação automática de dados para Excel.

> 💡 Projeto desenvolvido como **estudo de caso prático**, combinando um backend robusto (**Flask + SQLAlchemy**) com um frontend responsivo (**Bootstrap**) e automação de tarefas (**Pandas + Watchdog**).

---

## ✨ Funcionalidades Principais

✅ **CRUD de Produtos** — Cadastro, leitura e atualização de produtos (deleção ainda não implementada)  
✅ **Validação de EAN-13** — Confere se o código de barras possui exatamente 13 dígitos numéricos  
✅ **Controle de Estoque** — Registro manual de entradas (compras, recebimentos) e saídas (vendas, perdas)  
✅ **Tratamento de Erros** — Mensagens amigáveis sem interromper a aplicação  

### 📊 Relatórios Detalhados
- **Estoque Atual:** Visão em tempo real dos produtos e suas quantidades  
- **Relatório de Entradas:** Histórico de produtos adicionados ao estoque  
- **Relatório de Saídas:** Histórico de produtos retirados do estoque  

### ⚙️ Exportação Automática
A cada movimento de estoque, o sistema salva automaticamente o **relatório de estoque atual** em um arquivo Excel (`/data/estoque_atual.xlsx`).

### 🤖 Automação de Entrada (2 Formas)
1. **API Endpoint:** `/api/registrar_entrada` — Recebe dados JSON de outro sistema (ex: leitor de caixa)  
2. **Monitor de Pasta (Watcher):** Script `watcher.py` monitora a pasta `/watch_folder`.  
   Quando um arquivo `.xlsx` ou `.csv` é adicionado, o sistema registra as entradas automaticamente.

---

## 🚀 Tecnologias Utilizadas

### 🧠 Backend
- **Python 3**
- **Flask** — Microframework web
- **SQLAlchemy** — ORM para banco de dados

### 🗃️ Banco de Dados
- **SQLite** — Banco de dados leve baseado em arquivo

### 🎨 Frontend
- **HTML5**
- **Jinja2** — Template engine do Flask
- **Bootstrap 5** — Estilização responsiva

### ⚙️ Automação e Dados
- **Pandas** — Criação e exportação de relatórios Excel
- **Watchdog** — Monitoramento de arquivos (automação de entradas)

---

## 🧩 Estrutura do Projeto

```bash
gestor-estoque/
├── app.py
├── models.py
├── watcher.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── index.html
│   ├── cadastro.html
│   ├── relatorios.html
├── data/
│   └── estoque_atual.xlsx
└── watch_folder/
# Clone o repositório
git clone https://github.com/seu-usuario/gestor-estoque.git
cd gestor-estoque

# Crie um ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor Flask
python app.py
📦 Requisitos

Python 3.10+

Flask

SQLAlchemy

Pandas

Watchdog

Bootstrap 5

Todas as dependências estão listadas em requirements.txt

🧑‍💻 Autor

Lenilson José do Nascimento
📧 lenylson.nascimento@.com

💼 GitHub

🏁 Licença

Este projeto está licenciado sob a MIT License — veja o arquivo LICENSE
 para mais detalhes.
