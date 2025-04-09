import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import re
import os
from itertools import chain

#______________________________________________________________________________________________#

#Configurações do Streamlit

st.set_page_config(page_title='Verifica preenchimento - ALF - Aprova Digital', 
                   layout="centered", 
                   initial_sidebar_state='expanded',
                   page_icon=('images/favicon.png'), 
                   menu_items=None
                   )

logo_image = ('images/logo.png')

#Sidebar
st.sidebar.image(logo_image, width=150)
st.sidebar.divider()
st.sidebar.page_link("app.py", label="01_Consulta de Viabilidade (inscr.)")
st.sidebar.page_link("pages/cv_zona.py", label="__Consulta de Viabilidade (zona)")
st.sidebar.page_link("pages/verifica_aprova.py", label="02_Verifica processo ALF")
st.sidebar.page_link("pages/links.py", label="03_Links úteis")
st.sidebar.page_link("pages/documentacao-complementar-ALF.py", label="04_Doc. complementar ALF")
st.sidebar.page_link("pages/estudo-de-impacto-de-vizinhanca.py", label="05_EIV")
st.sidebar.page_link("pages/regin.py", label='06_REGIN - Alvará')
st.sidebar.page_link("pages/regin-viabilidade.py", label='07_REGIN - Viabilidade')
st.sidebar.page_link("pages/risco_regin.py", label='08_REGIN - Classificação de risco')


#Página principal do Streamlit - fixa
st.subheader('Classificação de risco e uso REGIN - Empresas e MEI')

ib_regin= st.text_input(
    "Cole todo o texto da página do REGIN",
    key="ib_regin"
    )

#Botão limpar

def clear_text():
    st.session_state["ib_regin"] = ""
st.button("Limpar", on_click=clear_text)

#______________________________________________________________________________________________#

#Tabelas CSV

df_cnaes=pd.read_csv("dados-regin/regin-cnaes-risco.csv", nrows=2000)
df_cad_imob=pd.read_csv("dados-regin/cad_imob.csv", nrows=300000)
df_risco_uso=pd.read_csv("dados/risco_uso.csv", nrows=2000)
df_zona_col=pd.read_csv("dados/zona_col.csv", nrows=100)
df_inscricao=pd.read_csv("dados/inscricao.csv")


#______________________________________________________________________________________________#


#Análise do processo
try:
    if ib_regin!= "":
        #Extrai informações do REGIN
        texto_regin_split = re.sub(' +', ' ',ib_regin).split(' ')

        #Reconhece os CNAEs e CNPJ
        cnaes_regin = re.findall(r'\d\d.\d\d-\d/\d\d', ib_regin)

        #Identifica os padrões da página
        index_regin3=texto_regin_split.index('Construída(m2):')


        #Extrai as informações
        area_construida_regin = " ".join(texto_regin_split[index_regin3+1:index_regin3+2])



        #______________________________________________________________________________________________#

        #Tabela de cnaes, risco e classificação de uso
        if area_construida_regin == 'Tipo':
            area_construida_regin = 0

        area_construida_regin = int(area_construida_regin)

        #Filtra a coluna de risco em função da área
        if area_construida_regin <= 150:
            id_risco='ate150.'
        if area_construida_regin > 150 and area_construida_regin <= 500:
            id_risco='150a500.'
        if area_construida_regin > 500 and area_construida_regin <= 750:
            id_risco='500a750.'
        if area_construida_regin > 750:
            id_risco='acima750.'
            
        #Filta a coluna de uso em função da área
        if area_construida_regin <= 150:
            id_uso='ate150'
        if area_construida_regin > 150 and area_construida_regin <= 200:
            id_uso='150a200'
        if area_construida_regin > 200 and area_construida_regin <= 500:
            id_uso='200a500'
        if area_construida_regin > 500 and area_construida_regin <= 750:
            id_uso='500a750'
        if area_construida_regin > 750 and area_construida_regin <= 1000:
            id_uso='750a1000'
        if area_construida_regin > 1000:
            id_uso='acima1000'
        
        df=pd.DataFrame(cnaes_regin)
        df.rename(columns={0: 'codigo'}, inplace=True)
        df_merge=pd.merge(df,df_cnaes,left_on='codigo',right_on='codigo-regin', how='inner')
        df_cnaes_risco_uso_selecionado = df_merge[['codigo-regin', 'denominacao', id_risco, id_uso]]
          

#______________________________________________________________________________________________#


        #Printa as verificações com o streamlit
        #Resumo do processo
        st.divider()

        #Análise de risco
        st.subheader('Classificação de risco e uso das atividades')
        st.dataframe(df_cnaes_risco_uso_selecionado, hide_index=True)

        st.divider()

except:
    st.markdown(''':red[1. Verifique se colou no campo as informações da aba 'GERAL'.]''')
    st.markdown(''':red[2. Verifique se colou no campo as informações considerando a aba 'ATIVIDADES EXERCIDAS']''')
