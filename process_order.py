# Programa para exportar o arquivo jSON formatado

import os
import json

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
                    raise ValueError(f"Volume item_id {volume.get('item_id')} está com 'quantity' inválido.")

    # Ajusta o campo "city" para que não seja uma lista
    importer = order_data.get("importer", {})
    addresses = importer.get("addresses", [])
    for address in addresses:
        if isinstance(address.get("city"), list) and len(address["city"]) > 0:
            address["city"] = address["city"][0]

    return order_data

# Função para exportar os dados para um arquivo JSON
def export_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Função para ler e ajustar os dados do arquivo JSON
def read_and_adjust_order_data(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        order_data = json.load(json_file)

    return adjust_json_format(order_data)

# Função principal para processar um arquivo JSON específico
def process_specific_json_file(file_path, output_folder):
    try:
        print(f"Lendo o arquivo JSON: {file_path}")

        # Lê e ajusta os dados do arquivo JSON
        adjusted_data = read_and_adjust_order_data(file_path)

        # Gera o nome do arquivo de saída com o mesmo nome do arquivo original
        output_filename = os.path.join(output_folder, os.path.basename(os.path.splitext(file_path)[0] + '_adjusted.json'))

        # Exporta os dados ajustados para o arquivo JSON
        export_to_json(adjusted_data, output_filename)
        print(f"Dados ajustados exportados para {output_filename}")

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o arquivo JSON {file_path}. Verifique o formato do arquivo.")
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo {file_path}: {e}")

# Caminho para a pasta que contém os arquivos JSON
folder_path = r'E:\Mile_Express\send'

# Caminho para a pasta de Downloads
downloads_folder = r'C:\Users\guilherme.meijomil\Downloads'

# Nome do arquivo JSON específico que você deseja processar
specific_json_file = '5164_23D308B4-C300-47B6-8CE1-E1F366E07B15.json'  # Substitua pelo nome do seu arquivo

# Caminho completo do arquivo JSON específico
file_path = os.path.join(folder_path, specific_json_file)

# Processa o arquivo JSON específico
process_specific_json_file(file_path, downloads_folder)

# O programa termina aqui
print("Processamento concluído.")
