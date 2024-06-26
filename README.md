<<<<<<< HEAD
# Dados de Empresas Brasil CNPJ

Este repositório contém scripts e dados relacionados ao processamento de informações de empresas no Brasil, utilizando o banco de dados de Cadastro Nacional da Pessoa Jurídica (CNPJ).

## Índice

- [Sobre](#sobre)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Sobre

O objetivo deste projeto é facilitar o processamento e análise de dados de empresas brasileiras a partir dos dados fornecidos pela Receita Federal. Utilizamos o banco de dados DuckDB para manipulação e consultas eficientes.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:  
  
```
├── src  
│ ├── data  
│ │ ├── extract  
│ │ │ ├── Socios  
│ │ │ │ └── arquivo  
│ │ │ ├── Estabelecimentos
│ │ │ │ └── arquivo  
│ │ │ └── ...
│ ├── raw
│ │  └── ingestion.py
│ ├── silver
│ │  └── silver.py 
│ ├── utils  
│ │ └── read_data_json.py  
│ ├── main.py  
│ └── columns_layout_cnpj_metadados.json  
└── README.md  
```



- `src/data/extract/`: Contém os arquivos CSV extraídos.
- `src/raw/ingestion.py`: Script para ingestão dos dados brutos.
- `src/silver/silver.py`: Script para processamento intermediário dos dados.
- `src/utils/read_data_json.py`: Script utilitário para leitura do arquivo JSON de metadados.
- `src/main.py`: Script principal para processamento dos dados.
- `columns_layout_cnpj_metadados.json`: Arquivo JSON contendo a estrutura das tabelas e colunas dos dados do CNPJ.

## Instalação

Para rodar este projeto localmente, siga os passos abaixo:

1. Clone o repositório:
    ```sh
    git clone https://github.com/s2breninn/dadosempresas-brasil-cnpj.git
    cd dadosempresas-brasil-cnpj
    ```

2. Instale o Poetry, se ainda não o tiver instalado:
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Instale as dependências do projeto usando o Poetry:
    ```sh
    poetry install
    ```

4. Ative o ambiente virtual do Poetry:
    ```sh
    poetry shell
    ```  

## Uso

### Ingestão de Dados Brutos

Execute o script de ingestão para carregar os dados brutos:

```sh
task ingestion
```


Execute o script para adicionar, organizar e nomear as colunas dos arquivos instalados:

```sh
task silver
```

=======
# Dados de Empresas Brasil - CNPJ

## Descrição
Este projeto visa construir um Datahouse para ingestão de dados de empresas com CNPJ a partir da base de dados do governo federal do Brasil.

!['Diagrama de fluxo da aplicação'](./assets/diagrama.png)

## Estrutura do Projeto
- **`src`**: Código fonte para processamento e ingestão de dados.
- **`utils`**: Funções auxiliares e utilitários.
- **`layout-cnpj-metadados.pdf`**: Documentação dos metadados dos arquivos CNPJ.
- **`.gitignore`**: Arquivos e diretórios ignorados pelo Git.
- **`poetry.lock` e `pyproject.toml`**: Configurações do Poetry para gerenciamento de dependências.

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal.
- **DuckDB**: Banco de dados analítico embutido.
- **Requests**: Biblioteca para fazer requisições HTTP.
- **BeautifulSoup**: Biblioteca para parsing de HTML.
- **Poetry**: Ferramenta para gerenciamento de dependências e packaging.
>>>>>>> 6ff937c3ca00f7d55696e2b657c99a01709f756b
