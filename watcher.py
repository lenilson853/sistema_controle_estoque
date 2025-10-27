import time
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app import create_app, db
from app.models import Produto
from app.services import registrar_movimento

# Pasta que será monitorada
WATCH_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'watch_folder')
if not os.path.exists(WATCH_PATH):
    os.makedirs(WATCH_PATH)

print(f"Monitorando a pasta: {WATCH_PATH}")

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Ignora se for um diretório
        if event.is_directory:
            return
            
        # Processa apenas arquivos .xlsx ou .csv
        if event.src_path.endswith('.xlsx') or event.src_path.endswith('.csv'):
            print(f"Novo arquivo detectado: {event.src_path}")
            time.sleep(1) # Espera 1s para garantir que o arquivo terminou de ser escrito
            processar_arquivo_entrada(event.src_path)

def processar_arquivo_entrada(filepath):
    """
    Lê o arquivo (Excel ou CSV) e registra as entradas no DB.
    Formato esperado no arquivo: Coluna 'codigo_barras' e Coluna 'quantidade'
    """
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
            
        # Requer contexto do app Flask para acessar o DB
        app = create_app()
        with app.app_context():
            for index, row in df.iterrows():
                try:
                    codigo = str(row['codigo_barras'])
                    qnt = int(row['quantidade'])
                    
                    produto = Produto.query.filter_by(codigo_barras=codigo).first()
                    
                    if produto:
                        motivo = f"Entrada automática via arquivo: {os.path.basename(filepath)}"
                        registrar_movimento(produto.id, 'entrada', qnt, motivo)
                        print(f"Registrado: {qnt}x {produto.nome}")
                    else:
                        print(f"AVISO: Produto com código {codigo} não encontrado no DB.")
                        
                except Exception as e:
                    print(f"Erro ao processar linha {index} do arquivo: {e}")
            
        # (Opcional) Mover ou deletar o arquivo após processar
        # os.remove(filepath) 
        print(f"Processamento do arquivo {filepath} concluído.")

    except Exception as e:
        print(f"Erro ao ler o arquivo {filepath}: {e}")


if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()