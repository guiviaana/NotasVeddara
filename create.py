import os
import glob
import requests
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

log_file_path = '/Users/guilherme/Downloads/processed_files.log'

# Função para obter o token de acesso
def get_access_token():
    token_url = 'https://191.235.65.21/oauth/token'
    login_data = {
        "grant_type": "password",
        "client_id": 1,
        "client_secret": "xwShEAUn6MJ82AZzaECmypbp6PmjTM3HPhDYaxE7",
        "username": "hml@veddara.com.br",
        "password": "SjXN6b8g3nS71",
        "scope": "*"
    }
    
    response = requests.post(token_url, headers={'Content-Type': 'application/json'}, json=login_data, verify=False)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Erro ao obter token: {response.status_code} - {response.text}")

# Função para criar a ordem de serviço
def create_order(access_token, order_data):
    order_url = 'https://191.235.65.21/v1/order-service/create'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(order_url, headers=headers, json=order_data, verify=False)
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Falha ao criar ordem de serviço: {response.status_code} - {response.text}")

# Função para exportar os dados para um arquivo JSON
def export_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Função para ler e ajustar os dados do arquivo JSON
def read_and_adjust_order_data(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        order_data = json.load(json_file)
    
    return adjust_json_format(order_data)

# Função para ajustar o formato do JSON
def adjust_json_format(order_data):
    # Ajustando o campo 'volumes' para ser uma lista de listas de dicionários
    if isinstance(order_data.get("volumes"), dict):
        order_data["volumes"] = [[order_data["volumes"]]]

    # Ajustando o campo 'city' para ser um dicionário único ao invés de uma lista
    importer = order_data.get("importer", {})
    addresses = importer.get("addresses", [])
    for address in addresses:
        if isinstance(address.get("city"), list) and len(address["city"]) > 0:
            address["city"] = address["city"][0]

    return order_data

# Função para carregar os arquivos processados do log
def load_processed_files(log_file):
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f.readlines())
    return set()

# Função para salvar os arquivos processados no log
def save_processed_file(log_file, filename):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(filename + '\n')

# Função principal para processar arquivos JSON
def process_json_file(json_file, access_token, processed_files):
    if json_file in processed_files:
        print(f"O arquivo {json_file} já foi processado. Ignorando...")
        return

    try:
        print(f"Processando arquivo: {json_file}")
        
        # Lê e ajusta os dados do arquivo JSON
        order_data = read_and_adjust_order_data(json_file)
        
        # Tenta criar a ordem de serviço
        try:
            order_result = create_order(access_token, order_data)
            print(f"Ordem de serviço criada com sucesso para {json_file}: {order_result}")
            
            # Gera o nome do arquivo de saída com o mesmo nome do arquivo original
            output_filename = os.path.join('/Users/guilherme/Downloads/Export', os.path.basename(os.path.splitext(json_file)[0] + '_result.json'))
            
            # Exporta os dados da ordem de serviço para um arquivo JSON
            export_to_json(order_result, output_filename)
            print(f"Dados exportados para {output_filename}")
            
            # Salva o arquivo no log de arquivos processados
            save_processed_file(log_file_path, json_file)

        except Exception as e:
            print(f"Erro ao criar ordem de serviço para o arquivo {json_file}: {e}")

    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON {json_file}. Verifique o formato do arquivo.")
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo {json_file}: {e}")

# Função para processar todos os arquivos JSON na pasta ao iniciar
def process_all_json_files_in_folder(folder_path):
    processed_files = load_processed_files(log_file_path)
    access_token = get_access_token()
    
    json_files = glob.glob(os.path.join(folder_path, '*.json'))
    
    for json_file in json_files:
        process_json_file(json_file, access_token, processed_files)

# Handler do watchdog para monitorar novos arquivos
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.processed_files = load_processed_files(log_file_path)
        self.access_token = get_access_token()
    
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.json'):
            process_json_file(event.src_path, self.access_token, self.processed_files)

# Função para monitorar a pasta e processar novos arquivos JSON
def monitor_folder(folder_path):
    event_handler = NewFileHandler(folder_path)
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Caminho para a pasta que contém os arquivos JSON
folder_path = '/Users/guilherme/Downloads/Send'

# Processa todos os arquivos JSON na pasta inicialmente
process_all_json_files_in_folder(folder_path)

# Monitora a pasta para novos arquivos
monitor_folder(folder_path)
