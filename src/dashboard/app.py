import streamlit as st
import duckdb
import os
import sys
sys.path.insert(0, os.getcwd())

df_empresas = duckdb.execute(f'SELECT * FROM  "src/data/silver.parquet/Empresas.parquet" LIMIT 50').df()
df_estabelecimentos = duckdb.execute(f'SELECT concat(cnpj_basico, cnpj_ordem, cnpj_dv) AS cnpj, * FROM  "src/data/silver.parquet/Estabelecimentos.parquet" LIMIT 50').df()
df_cnaes = duckdb.execute(f'SELECT * FROM  "src/data/silver.parquet/Cnaes.parquet" LIMIT 50').df()
df_motivos = duckdb.execute(f'SELECT * FROM  "src/data/silver.parquet/Motivos.parquet" LIMIT 50').df()
df_municipios = duckdb.execute(f'SELECT * FROM  "src/data/silver.parquet/Municipios.parquet"').df()

pag1 = 'Empresas'
pag2 = 'Estabelecimentos'
pag3 = 'Cnaes'
pag4 = 'Motivos'
pag5 = 'Municipios'

st.set_page_config('Dados CNPJ - RFB', layout='wide', page_icon=':shark:')

with st.sidebar:
    st.title('Dados de empresas brasileiras')
    st.caption(f'''Seja bem vindo(a) a nossa aplicação de dados abertos da Receita Federal Brasileira. Nosso intuito é o foco na análise de empresas para diversos cenários. 
               \n\nEx.: Quantas farmacias tem na cidade de Teófilo Otoni?
               \n\nCom essas perguntas e análises você terá uma visão melhor sobre seu negócio.''')
    
tab1, tab2, tab3, tab4, tab5 = st.tabs([pag1, pag2, pag3, pag4, pag5])

with tab1:
   st.header("Empresas")
   st.dataframe(df_empresas)

with tab2:
   st.header("Estabelecimentos")
   st.dataframe(df_estabelecimentos)

with tab3:
   st.header("Cnaes")
   st.dataframe(df_cnaes)

with tab4:
   st.header("Motivos")
   st.dataframe(df_motivos)

with tab5:
   st.header("Municipios")
   st.dataframe(df_municipios)