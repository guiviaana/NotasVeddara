# Programa para criar ordem de pedido na mileexpress

import os
import glob
import requests
import json
import time

log_file_path = r'E:\Mile_Express\logs\processed_files.log'
error_log_file_path = r'E:\Mile_Express\logs\error_files.log'

# Variáveis de contagem
json_count = 0
success_count = 0

# Função para obter o token de acesso


def get_access_token():
    token_url = 'https://api.mileexpress.com.br/oauth/token'
    login_data = {
        "grant_type": "password",
        "client_id": 1,
        "client_secret": "xwShEAUn6MJ82AZzaECmypbp6PmjTM3HPhDYaxE7",
        "username": "veddara_integration@veddare.com.br",
        "password": "32_s0{O)oFr!xuNy,EkY.LF",
        "scope": "*"
    }

    response = requests.post(
        token_url, headers={'Content-Type': 'application/json'}, json=login_data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(
            f"Erro ao obter token: {response.status_code} - {response.text}")

# Função para criar a ordem de serviço


def create_order(access_token, order_data):
    order_url = 'https://api.mileexpress.com.br/v1/order-service/create'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(order_url, headers=headers,
                             json=order_data, verify=False)

    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(
            f"Falha ao criar ordem de serviço: {response.status_code} - {response.text}")

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
    # Ajusta o campo "volumes" para ser uma lista de listas
    volumes = order_data.get("volumes")

    if isinstance(volumes, dict):
        # Caso volumes seja um dicionário, converte para lista de listas
        order_data["volumes"] = [[volumes]]
    elif isinstance(volumes, list):
        # Caso volumes seja uma lista, converte para lista de listas
        order_data["volumes"] = [[volume] for volume in volumes]

        # Verifica se todos os volumes possuem o campo "quantity" com valor válido
        for volume_list in order_data["volumes"]:
            for volume in volume_list:
                if "quantity" not in volume or volume["quantity"] is None or volume["quantity"] == "":
                    raise ValueError(
                        f"Volume item_id {volume.get('item_id')} está com 'quantity' inválido.")

    # Ajusta o campo "city" para que não seja uma lista
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

# Função para salvar os arquivos com erros no log de erros


def save_error_file(log_file, filename, error_message):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{filename}: {error_message}\n")

# Função principal para processar arquivos JSON


def process_json_file(json_file, access_token, processed_files):
    global json_count, success_count

    if json_file in processed_files:
        print(f"O arquivo {json_file} já foi processado. Ignorando...")
        return

    json_count += 1  # Incrementa a contagem de JSON lidos

    try:
        print(f"Processando arquivo: {json_file}")

        # Lê e ajusta os dados do arquivo JSON
        order_data = read_and_adjust_order_data(json_file)

        # Tenta criar a ordem de serviço
        try:
            order_result = create_order(access_token, order_data)
            print(
                f"Ordem de serviço criada com sucesso para {json_file}: {order_result}")

            # Gera o nome do arquivo de saída com o mesmo nome do arquivo original
            output_filename = os.path.join(r'E:\Mile_Express\received', os.path.basename(
                os.path.splitext(json_file)[0] + '_result.json'))

            # Exporta os dados da ordem de serviço para um arquivo JSON
            export_to_json(order_result, output_filename)
            print(f"Dados exportados para {output_filename}")

            # Salva o arquivo no log de arquivos processados
            save_processed_file(log_file_path, json_file)

            success_count += 1  # Incrementa a contagem de ordens criadas com sucesso

        except Exception as e:
            print(
                f"Erro ao criar ordem de serviço para o arquivo {json_file}: {e}")
            save_error_file(error_log_file_path, json_file, str(e))

    except json.JSONDecodeError as e:
        print(
            f"Erro ao decodificar o arquivo JSON {json_file}. Verifique o formato do arquivo.")
        save_error_file(error_log_file_path, json_file,
                        f"JSONDecodeError: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo {json_file}: {e}")
        save_error_file(error_log_file_path, json_file, str(e))

# Função para processar todos os arquivos JSON na pasta ao iniciar


def process_all_json_files_in_folder(folder_path):
    global json_count, success_count
    processed_files = load_processed_files(log_file_path)
    access_token = get_access_token()

    json_files = glob.glob(os.path.join(folder_path, '*.json'))

    for json_file in json_files:
        process_json_file(json_file, access_token, processed_files)

    # Exibe o resultado das contagens
    print(f"Total de arquivos JSON lidos: {json_count}")
    print(f"Total de ordens criadas com sucesso: {success_count}")


# Caminho para a pasta que contém os arquivos JSON
folder_path = r'E:\Mile_Express\send'

# Processa todos os arquivos JSON na pasta inicialmente
process_all_json_files_in_folder(folder_path)

# O programa termina aqui
print("Processamento concluído.")
