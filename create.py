import requests
import json

# Função para obter o token de acesso
def get_access_token():
    token_url = 'https://dev.mileexpress.com.br/oauth/token'
    login_data = {
        "grant_type": "password",
        "client_id": 1,
        "client_secret": "xwShEAUn6MJ82AZzaECmypbp6PmjTM3HPhDYaxE7",
        "username": "hml@veddara.com.br",
        "password": "SjXN6b8g3nS71",
        "scope": "*"
    }
    
    response = requests.post(token_url, headers={'Content-Type': 'application/json'}, json=login_data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Erro ao obter token: {response.status_code} - {response.text}")

# Função para criar a ordem de serviço
def create_order(access_token):
    order_url = 'https://dev.mileexpress.com.br/v1/order-service/create'
    order_data = {
    "volumes": [
        [
            {
                "item_id": "44",
                "description": "POMADA 20mg",
                "sku": "4456456456456546456",
                "commercial_value": 18.87,
                "quantity": "1",
                "customs_tax_classes_id": 11,
                "customs_administrative_processes_id": "1"
            }
        ]
    ],
    "description": "POMADA  20mg",
    "freight": 35.85,
    "commercial_value": 18.87,
    "currency_id": 2,
    "importer": {
        "name": "teste maior segundo",
        "addresses": [
            {
                "number": 432,
                "additional_info": None,
                "country_id": 35,
                "zip_code": "8805",
                "address": "Rua",
                "city": {
                    "name": "FlorianÃ³polis",
                    "uf": "SC"
                },
                "neighborhood": "Sa"
            }
        ],
        "documents": [
            {
                "type": "CPF",
                "number": "111111111111"
            }
        ],
        "email": [
            {
                "address": "teste@segundo.com"
            }
        ]
    },
    "status_order": "ativo",
    "company_id": "1",
    "integration": True,
    "by_pass_stock": True,
    "shipper_id": "1031"
}
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(order_url, headers=headers, json=order_data)
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Falha ao criar ordem de serviço: {response.status_code} - {response.text}")

# Fluxo principal do programa
try:
    # Obtém o token de acesso
    access_token = get_access_token()
    print("Token obtido com sucesso:", access_token)
    
    # Adicionando log para verificar o fluxo
    print("Criando ordem de serviço...")
    
    # Cria a ordem de serviço usando o token obtido
    order_result = create_order(access_token)
    print("Ordem de serviço criada com sucesso:", order_result)
    
except Exception as e:
    print(f"Erro: {e}")
