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
        self.parquet_folder = os.path.join(base_directory, 'silver.parquet')

    def create_folder(self, folder_path: str) -> None:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Diretório criado em: {folder_path}')
        else:
            print(f'Diretório já existe: {folder_path}')

    def connect_database(self):
        try:
            conn = duckdb.connect(database='dbrfbcnpj.db', read_only=False)
            return conn
        except duckdb.Error as e:
            raise RuntimeError(f"Erro ao conectar no banco de dados: {e}")

    def create_table(self, table_name: str, path_file_name_parquet: str):
        try:
            self.connection.execute(f'CREATE TABLE "{table_name}" AS SELECT * FROM "{path_file_name_parquet}"')
            print(f'Tabela {table_name} criada com sucesso.')
        except duckdb.Error as e:
            print(f'Erro ao criar tabela {table_name}: {e}')

    def csv_to_parquet(self, dir_path_full_data_csv: str, columns: list, path_file_name_parquet: str):
        query = f"""
            COPY (
                SELECT * FROM read_csv_auto(
                    '{dir_path_full_data_csv}',
                    normalize_names=true,
                    ignore_errors=true,
                    delim=';',
                    header=true,
                    names={columns}
                    )
            ) TO '{path_file_name_parquet}' (FORMAT PARQUET)
        """
        try:
            self.connection.execute(query)
            print(f"Convertido {dir_path_full_data_csv} CSV para PARQUET: {self}")
        except duckdb.Error as e:
            print(f'Erro ao processar arquivo {dir_path_full_data_csv}: {e}')

    def process_files(self):
        for root, dirs, _ in os.walk(self.extracted_folder):
            for dir in dirs:

                table_info = self.json_data['tabelas'].get(dir)

                if table_info:
                    table_name, columns = table_info[0]['nome'], table_info[0]['colunas']
                    dir_path_full_data_csv = os.path.join(root, dir, '*')

                    file_name_parquet = f"{table_name}.parquet"
                    path_file_name_parquet = os.path.join(self.parquet_folder, file_name_parquet)

                    self.csv_to_parquet(dir_path_full_data_csv, columns, path_file_name_parquet)
                    self.create_table(table_name, path_file_name_parquet)

    def process_data(self):
        self.create_folder(self.parquet_folder)
        self.process_files()

if __name__ == '__main__':
    base_directory = os.path.join('src', 'data') 
    path_file_json = './src/columns_layout_cnpj_metadados.json'

    json_data = read_data_json(path_file_json)

    processor = DataProcessor(base_directory, json_data)
    processor.process_data()
