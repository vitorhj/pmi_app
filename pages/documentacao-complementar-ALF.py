import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import re
import os
from itertools import chain

#Configurações do Streamlit

st.set_page_config(page_title='Viabilidade ALF Itajaí', 
                   layout="centered", 
                   initial_sidebar_state='expanded',
                   page_icon=('favicon.png'), 
                   menu_items=None
                   )

logo_image = ('logo.png')

#Sidebar
st.sidebar.page_link("viabilidade_empresas.py", label="")
st.sidebar.page_link("pages/verifica_aprova.py", label="")
st.sidebar.page_link("pages/links.py", label="")
st.sidebar.page_link("pages/documentacao-complementar-ALF.py", label="")

#Tabelas CSV

df_docs=pd.read_csv("relacao_docs_alf.csv")

#Página principal do Streamlit - fixa

st.image(logo_image, width=150)
st.subheader('Documentação complementar - ALF - Aprova Digital')

ib_cnpj = st.text_input(
    "Cole todo o texto do CNPJ",
    key="ib_cnpj"
    )

#Botão limpar

def clear_text():
    st.session_state["ib_aprova"] = ""
    st.session_state["ib_cnpj"] = ""
st.button("Limpar", on_click=clear_text)

#Análise da documentação complementar
try:
    if ib_cnpj != "":
        cnaes_cnpj = re.findall(r'\d\d.\d\d-\d-\d\d', ib_cnpj)
        cnae_principal_cnpj=cnaes_cnpj[0]
        numero_cnpj = re.findall(r'\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d', ib_cnpj)
        texto_cnpj_split = re.sub(' +', ' ',ib_cnpj).split(' ')
        itens_analise=['EMPRESARIAL','TÍTULO', 'LOGRADOURO','NÚMERO']
        index_cnpj1=texto_cnpj_split.index('EMPRESARIAL')+1
        index_cnpj2=texto_cnpj_split.index('TÍTULO')
        razao_social_cnpj = " ".join(texto_cnpj_split[index_cnpj1:index_cnpj2])
        index_cnpj3=texto_cnpj_split.index('NATUREZA')+1
        index_cnpj4=texto_cnpj_split.index('ESPECIAL')
        texto_cnpj_split2 = texto_cnpj_split[index_cnpj3:index_cnpj4] #função que separa o primeiro split
        index_cnpj5=texto_cnpj_split2.index('LOGRADOURO')+1
        index_cnpj6=texto_cnpj_split2.index('NÚMERO')
        logradouro_cnpj = " ".join(texto_cnpj_split2[index_cnpj5:index_cnpj6])
        index_cnpj7=texto_cnpj_split2.index('NÚMERO')+1
        index_cnpj8=texto_cnpj_split2.index('COMPLEMENTO')
        numeropredial_cnpj = " ".join(texto_cnpj_split2[index_cnpj7:index_cnpj8])
        index_cnpj9=texto_cnpj_split2.index('COMPLEMENTO')+1
        index_cnpj10=texto_cnpj_split2.index('CEP')
        complemento_cnpj = " ".join(texto_cnpj_split2[index_cnpj9:index_cnpj10])
        index_cnpj11=texto_cnpj_split2.index('BAIRRO/DISTRITO')+1
        index_cnpj12=texto_cnpj_split2.index('MUNICÍPIO')
        bairro_cnpj = " ".join(texto_cnpj_split2[index_cnpj11:index_cnpj12])

        st.text(cnaes_cnpj)
        
        cnaes_cnpj=pd.DataFrame(cnaes_cnpj)
        st.dataframe(cnaes_cnpj)
        cnaes_cnpj = cnaes_cnpj.rename(columns={'': 'codigo'})
        df_filtrado=df_docs.merge(cnaes_cnpj,left_on='codigo', right_on='codigo')
        st.dataframe(df_filtrado)

except:
    st.markdown(''':red[Verifique o correto preenchimento de todos os campos.]''')
