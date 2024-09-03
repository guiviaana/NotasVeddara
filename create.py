import os
import glob
import requests
import json

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

# Função para ler os dados do arquivo JSON
def read_order_data_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

# Função principal para processar todos os arquivos JSON em uma pasta
def process_json_files_in_folder(folder_path, export_folder_path):
    try:
        # Obtém o token de acesso
        access_token = get_access_token()
        print("Token obtido com sucesso:", access_token)

        # Encontra todos os arquivos JSON na pasta
        json_files = glob.glob(os.path.join(folder_path, '*.json'))
        total_files = len(json_files)
        processed_files = 0
        
        print(f"Arquivos JSON encontrados: {json_files}")

        for json_file in json_files:
            print(f"Processando arquivo: {json_file}")
            
            try:
                # Lê os dados do arquivo JSON
                order_data = read_order_data_from_file(json_file)
                
                # Tenta criar a ordem de serviço
                try:
                    order_result = create_order(access_token, order_data)
                    print(f"Ordem de serviço criada com sucesso para {json_file}: {order_result}")
                    
                    # Gera o nome do arquivo de saída com o mesmo nome do arquivo original
                    output_filename = os.path.join(export_folder_path, os.path.splitext(os.path.basename(json_file))[0] + '_result.json')
                    
                    # Exporta os dados da ordem de serviço para um arquivo JSON
                    export_to_json(order_result, output_filename)
                    print(f"Dados exportados para {output_filename}")
                    
                    processed_files += 1

                except Exception as e:
                    # Captura o erro ao criar a ordem de serviço e continua o loop
                    print(f"Erro ao criar ordem de serviço para o arquivo {json_file}: {e}")
                    print("Continuando para o próximo arquivo...")
                    continue  # Garante que o loop continue para o próximo arquivo
            
            except json.JSONDecodeError:
                print(f"Erro ao decodificar o arquivo JSON {json_file}. Verifique o formato do arquivo.")
                print("Continuando para o próximo arquivo...")
                continue  # Continua para o próximo arquivo
            except Exception as e:
                print(f"Erro inesperado ao processar o arquivo {json_file}: {e}")
                print("Continuando para o próximo arquivo...")
                continue  # Continua para o próximo arquivo
        
        print(f"Todos os arquivos foram processados. Total de arquivos processados: {processed_files} de {total_files}.")
    
    except Exception as e:
        print(f"Erro ao obter o token ou ao processar a pasta: {e}")

# Caminho para a pasta que contém os arquivos JSON e a pasta de exportação
input_folder_path = '/Users/guilherme/Downloads/Send'
export_folder_path = '/Users/guilherme/Downloads/Export'

# Garante que a pasta de exportação existe
os.makedirs(export_folder_path, exist_ok=True)

process_json_files_in_folder(input_folder_path, export_folder_path)
