import requests
import json

# Endpoint e dados de login para obter o token
token_url = 'https://dev.mileexpress.com.br/oauth/token'
login_data = {
    "grant_type": "password",
    "client_id": 1,
    "client_secret": "xwShEAUn6MJ82AZzaECmypbp6PmjTM3HPhDYaxE7",
    "username": "hml@veddara.com.br",
    "password": "SjXN6b8g3nS71",
    "scope": "*"
}

# Requisição para obter o token
response = requests.post(token_url, headers={'Content-Type': 'application/json'}, json=login_data)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    token = response.json()['access_token']
    print("Token obtido com sucesso:", token)

    # Dados da ordem a ser criada (substitua pelos seus dados)
    order_data = {
        "volumes": [
            {
                "item_id": "44",
                "description": "POMADA 20mg",
                "sku": "4456456456456546456",
                "commercial_value": 18.87,
                "quantity": "1",
                "customs_tax_classes_id": 11,
                "customs_administrative_processes_id": "1"
            }
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
                        "name": "Florianópolis",
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
        "shipper_id": "1"
    }

    # URL do endpoint para criar uma ordem
    order_create_url = 'https://dev.mileexpress.com.br/v1/order-service/create'

    # Headers com o token de autorização
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
        
    }

    # Enviar a requisição POST com os dados da ordem
    response = requests.post(order_create_url, headers=headers, json=order_data)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("Ordem criada com sucesso!")
        print("Resposta:", response.json())
    else:
        print("Erro ao criar a ordem:", response.json())

else:
    print("Erro ao obter o token:", response.json())
