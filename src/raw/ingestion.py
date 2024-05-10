import os
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
        for zip_file in zip_files:
            zip_file = f'src/data/zip/{zip_file}'
            try:
                # Verifica se o arquivo ZIP existe
                if os.path.exists(zip_file):
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        # Cria o diretório 'extracted' para os arquivos extraídos
                        extract_folder = self.extracted_folder
                        
                        zip_ref.extractall(extract_folder)
                        print(f'Arquivos de {zip_file} extraídos para: {extract_folder}')
                else:
                    print(f'O arquivo {zip_file} não existe.')
            except Exception as e:
                print(f"Erro ao extrair o arquivo '{zip_file}': {e}")

    def ingest_data(self) -> None:
        #links = self.extract_links()
        #zip_files = self.download_files(links)
        zip_files = ['Empresas0.zip', 'Empresas0.ziplm7_i9u1.tmp', 'Empresas6.zip', 'Empresas3.zip', 'Estabelecimentos0.zip', 'Empresas1.zip', 'Empresas9.zip', 'Empresas7.zip', 'Cnaes.zip', 'Empresas5.zip', 'Empresas4.zip', 'Estabelecimentos2.zip', 'Estabelecimentos3.zip', 'Estabelecimentos4.zipms3j0jsb.tmp', 'Estabelecimentos1.zip', 'Empresas8.zip', 'Empresas2.zip']
        self.extract_files(zip_files)

if __name__ == '__main__':
    base_directory = os.path.join('src', 'data') 
    base_url = 'https://dadosabertos.rfb.gov.br/CNPJ/'

    ingestor = DataIngestor(base_url, base_directory)
    ingestor.ingest_data()