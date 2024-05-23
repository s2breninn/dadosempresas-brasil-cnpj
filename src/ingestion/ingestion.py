import os
import re
import shutil
import requests
import wget
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List

class DataIngestor:
    def __init__(self, base_url: str, base_directory: str) -> None:
        self.base_url = base_url
        self.base_directory = base_directory
        self.zip_folder = os.path.join(base_directory, 'zip')
        self.extracted_folder = os.path.join(base_directory, 'extracted')
        
        self.create_folder(self.zip_folder)
        self.create_folder(self.extracted_folder)

    def create_folder(self, folder_path: str) -> None:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Diretório criado em: {folder_path}')
        else:
            print(f'Diretório já existe: {folder_path}')

    def extract_links(self) -> List[str]:
        res = requests.get(self.base_url)
        soup = BeautifulSoup(res.text, 'html.parser')

        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.zip'):
                full_url = urljoin(self.base_url, href)
                links.append(full_url)
                
        return links

    def download_files(self, links: List[str]) -> List[str]:
        downloaded_files = []

        for link in links:
            zip_file_path = os.path.join(self.zip_folder, link.split('/')[-1])
            
            if self.file_exists(zip_file_path):
                print(f'O arquivo {zip_file_path} já existe.')
                downloaded_files.append(zip_file_path)
            else:
                try:
                    print(f'Baixando {zip_file_path}...')
                    wget.download(link, zip_file_path)
                    print(f' - Arquivo baixado com sucesso: {zip_file_path}')
                    downloaded_files.append(zip_file_path)
                except Exception as e:
                    print(f" - Erro ao baixar o arquivo '{zip_file_path}': {e}")
        
        return downloaded_files

    def file_exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)

    def extract_files(self, zip_files: List[str]) -> None:
        processed_and_extracted_files = []

        for (root, dirs, files), zip_file in zip(os.walk(self.extracted_folder), zip_files):
            try:
                if self.file_exists(zip_file):
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        extract_folder = self.create_directory_by_file_name(zip_file)
                        
                        zip_ref.extractall(extract_folder)
                        print(f'Arquivos de {zip_file} extraídos para: {extract_folder}')
                        
                        for file in files:
                            if file not in processed_and_extracted_files:
                                file_processed_utf8 = self.fix_uft8_encoding(root, file)
                                if file_processed_utf8 is not None:
                                    processed_and_extracted_files.append(file_processed_utf8)
                else:
                    print(f'O arquivo {zip_file} não existe.')
            except Exception as e:
                print(f"Erro ao extrair o arquivo '{zip_file}': {e}")
    
    def fix_uft8_encoding(self, root, file) -> None:
        try:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', errors='replace') as f:
                content = f.read()
                with open(file_path, 'w', encoding='utf-8') as wf:
                    wf.write(content)
            print(f'{file_path} convertido para UTF-8.')
            return file_path
        except UnicodeTranslateError as e:
            print(f'Erro ao converter unicode UTF-8: {e}')

    def create_directory_by_file_name(self, zip_file: str) -> str:
        file_name = re.sub(r'\.zip$', '', zip_file.split('/')[-1])
        directory_name = ''.join(re.findall('[a-zA-Z]', file_name))

        directory_path = os.path.join(self.extracted_folder, directory_name)

        self.create_folder(directory_path)

        return directory_path

    def delete_zip_files(self) -> None:
        try:
            shutil.rmtree(self.zip_folder)
            print(f'Diretório {self.zip_folder} deletado com sucesso.')
        except OSError as o:
            print(f'Error, {o.strerror}: {self.zip_folder}')

    def ingest_data(self) -> None:
        links = self.extract_links()
        zip_files = self.download_files(links)
        self.extract_files(zip_files)
        #self.delete_zip_files()

if __name__ == '__main__':
    base_directory = os.path.join('src', 'data') 
    base_url = 'https://dadosabertos.rfb.gov.br/CNPJ/'

    ingestor = DataIngestor(base_url, base_directory)
    ingestor.ingest_data()