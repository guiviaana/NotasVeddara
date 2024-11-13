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

# URL de consulta de estoque
url = 'https://api.mileexpress.com.br/v1/warehouse/stock'

# Obter token de acesso
access_token = get_access_token()

# Cabeçalhos com o token de acesso
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Realizar requisição GET para obter os dados de estoque
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Defina o caminho do arquivo de saída JSON
    file_path = os.path.join('E:\\Mile_Express\\Estoque', 'response.json')

    # Salvar a resposta JSON em um arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)

    print(f"Resposta salva em {file_path}")
else:
    print(f"Erro: {response.status_code} - {response.text}")
