import json

def read_data_json(path_file: str):
    try:
        with open(f"{path_file}", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f'Erro ao ler arquivo JSON: {path_file} | Error: {e}')

    return data