import os
import sys
import duckdb
sys.path.insert(0, os.getcwd())
from utils.read_data_json import read_data_json

class DataProcessor:
    def __init__(self, base_directory: str, json_data: dict):
        self.connection = self.connect_database()
        self.json_data = json_data
        self.extracted_folder = os.path.join(base_directory, 'extracted')

    def connect_database(self):
        try:
            conn = duckdb.connect(database='dbrfbcnpj.db', read_only=False)
            return conn
        except duckdb.Error as e:
            raise RuntimeError(f"Erro ao conectar no banco de dados: {e}")

    def create_table(self, table_name: str, df):
        try:
            self.connection.execute(f'CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df')
            print(f'Tabela {table_name} criada com sucesso.')
        except duckdb.Error as e:
            print(f'Erro ao criar tabela {table_name}: {e}')

    def process_files(self):
        for root, dirs, _ in os.walk(self.extracted_folder):
            for dir in dirs:
                table_info = self.json_data['tabelas'].get(dir)
                if table_info:
                    table_name, columns = table_info[0]['nome'], table_info[0]['colunas']
                    dir_path_full_data = os.path.join(root, dir, '*')
                    self.process_file(dir_path_full_data, columns)

    def process_file(self, file_path: str, columns: list):
        query = f"""
            SELECT *
            FROM read_csv_auto(
                '{file_path}',
                normalize_names=true,
                ignore_errors=true,
                delim=';',
                header=true,
                names={columns}
            )
            LIMIT 20
        """
        try:
            result_df = self.connection.execute(query).df()
            print(f"\nDados de {file_path}:\n", result_df)
        except duckdb.Error as e:
            print(f'Erro ao processar arquivo {file_path}: {e}')

    def process_data(self):
        self.process_files()

if __name__ == '__main__':
    base_directory = os.path.join('src', 'data') 
    path_file_json = './src/columns_layout_cnpj_metadados.json'

    json_data = read_data_json(path_file_json)

    processor = DataProcessor(base_directory, json_data)
    processor.process_data()
