import json
import os

# Nome do arquivo para salvar os dados
DATA_FILE = "despesas.json"

# Função para carregar dados de um arquivo JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Função para salvar dados em um arquivo JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)