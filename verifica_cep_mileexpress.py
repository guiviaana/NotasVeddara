# Código para ler o JSON contendo o CEP no arquivo tracking.json na pasta do SQLSRV23

import os
import json
import requests

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

    response = requests.post(token_url, headers={'Content-Type': 'application/json'}, json=login_data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Erro ao obter token: {response.status_code} - {response.text}")

# Função para verificar o CEP
def check_cep(cep):
    url = 'https://api.mileexpress.com.br/v1/cep/check'
    
    # Obter o token de acesso
    access_token = get_access_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        "cep": cep
    }

    # Fazendo a requisição POST
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro: {response.status_code} - {response.text}")

# Função para processar o arquivo cep.json e salvar cep_return.json
def process_cep_file(input_folder):
    input_filepath = os.path.join(input_folder, "cep.json")
    output_filepath = os.path.join(input_folder, "cep_return.json")

    # Verificar se o arquivo cep.json existe
    if not os.path.exists(input_filepath):
        print(f"Arquivo {input_filepath} não encontrado.")
        return

    # Ler o arquivo cep.json
    with open(input_filepath, 'r') as file:
        cep_data = json.load(file)

    cep = cep_data.get("cep")
    if not cep:
        print("O arquivo cep.json não contém o campo 'cep'.")
        return

    try:
        # Verificar o CEP
        response_data = check_cep(cep)

        # Salvar a resposta no arquivo cep_return.json, sem conversão de caracteres especiais
        with open(output_filepath, 'w', encoding='utf-8') as response_file:
            json.dump(response_data, response_file, ensure_ascii=False, indent=4)

        print(f"Resposta salva em {output_filepath}")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Caminho da pasta de entrada
input_folder = r"E:\Mile_Express\Valida_CEP"

# Processar o arquivo cep.json
process_cep_file(input_folder)
