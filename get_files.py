# Exporta o JSON recebido com os PDFs do pedido com método get

import requests
import json
import os

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

def get_order_service_file(order_id):
    # Obtendo o token de acesso
    access_token = get_access_token()
    
    # URL da API com o ID da ordem de serviço
    url = f"https://api.mileexpress.com.br/v1/order-service/files/{order_id}"
    
    # Cabeçalhos de autenticação com o token obtido
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Fazendo a requisição GET
        response = requests.get(url, headers=headers)
        
        # Verifica se a resposta foi bem-sucedida (status code 200)
        if response.status_code == 200:
            # Obter o conteúdo da resposta
            data = response.json()

            # Definir o caminho do arquivo JSON
            file_path = os.path.join(os.getcwd(), f"order_service_{order_id}.json")
            
            # Salvar os dados em um arquivo JSON
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Dados salvos no arquivo: {file_path}")
            return data
        else:
            # Trata outros status codes (erros)
            print(f"Erro na requisição: {response.status_code} - {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None

# Exemplo de uso
order_id = 16132
order_service_file = get_order_service_file(order_id)

if order_service_file:
    print("Resposta da API:", order_service_file)
