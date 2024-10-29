import requests
import json
import os

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

# Caminho do arquivo de entrada e saída
input_file = r"E:\Mile_Express\Tracking\tracking.json"
output_file = r"E:\Mile_Express\Tracking\tracking_return.json"

# Ler o código de rastreamento do arquivo JSON
with open(input_file, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    code_tracking = data.get("code_tracking")
    if not code_tracking:
        raise ValueError("O campo 'code_tracking' não foi encontrado no arquivo tracking.json")

# Obter token de acesso
access_token = get_access_token()

# Endpoint de rastreamento com o código lido do arquivo
url = f"https://api.mileexpress.com.br/v1/airwaybills/tracking?codes={code_tracking}"

# Cabeçalhos da requisição
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Requisição GET
response = requests.get(url, headers=headers)

# Verificar resposta e salvar no formato JSON
if response.status_code == 200:
    tracking_data = response.json()
    with open(output_file, "w", encoding="utf-8") as json_output:
        json.dump(tracking_data, json_output, ensure_ascii=False, indent=4)
    print(f"Dados do rastreamento salvos em '{output_file}'")
else:
    print(f"Erro ao obter dados: {response.status_code} - {response.text}")
