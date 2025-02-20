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
st.sidebar.page_link("pages/regin.py", label='06_REGIN')


#Página principal do Streamlit - fixa
st.subheader('Verifica REGIN')

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
        cnaes_regin = re.findall(r'\d\d.\d\d-\d/\d\d', ib_regin)
        cnpj_regin = re.findall(r'\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d', ib_regin)
        
        index_regin1=texto_regin_split.index('Empresarial:')
        index_regin2=texto_regin_split.index('Logradouro:')
        index_regin3=texto_regin_split.index('Construída(m2):')
        index_regin4=texto_regin_split.index('Fantasia:')
        index_regin5=texto_regin_split.index('Complemento:')
        index_regin6=texto_regin_split.index('Bairro:')
        index_regin7=texto_regin_split.index('Município:')


        razao_social_regin = " ".join(texto_regin_split[index_regin1+1:index_regin4-1])
        area_construida_regin = " ".join(texto_regin_split[index_regin3+1:index_regin3+2])
        logradouro_regin = " ". join(texto_regin_split[index_regin2+2:index_regin5-1])
        bairro_regin = " ". join(texto_regin_split[index_regin6+1:index_regin7])
        numero_predial_regin = " ".join(texto_regin_split[index_regin5-1:index_regin5])
        numero_predial_regin = numero_predial_regin.replace("Nº", "")
        logr_num_regin = logradouro_regin+' '+numero_predial_regin

        #______________________________________________________________________________________________#

        # Procura pela inscrição a partir do endereço informado no REGIN na tabela df_cad_imob
        df_filtrado = df_cad_imob.loc[df_cad_imob['logr_numpredial'] == logr_num_regin, ['Insc. Red', 'logr_numpredial']]
        df_filtrado1 = df_cad_imob.loc[df_cad_imob['logr_numpredial'] == logr_num_regin, ['Insc. Red']]
        inscr_regin = df_filtrado1['Insc. Red'].unique()
        inscr_regin = inscr_regin[0]
        inscr_arcgis = inscr_regin.replace('.', '')

        #______________________________________________________________________________________________#

        #Procura o zoneamento a partir da inscrição
        df_filtro_zoneamento = df_inscricao.loc[df_inscricao['inscricao'] == inscr_regin, ['zon_alv']]
        zon_regin = df_filtro_zoneamento['zon_alv'].unique()
        zon_regin = zon_regin[0]

        #______________________________________________________________________________________________#

        #Tabela de cnaes, risco e classificação de uso
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

        #Procura a permissão pelo zoneamento
        df_filtro_permissao = df_risco_uso.loc[df_risco_uso['ZONA']==zon_regin]

        #______________________________________________________________________________________________#

        #Filtra os usos com base na área
        df_class_uso = df_cnaes_risco_uso_selecionado[id_uso]
        class_uso = df_cnaes_risco_uso_selecionado[id_uso].unique().tolist()
        class_uso=''.join(class_uso)


        #______________________________________________________________________________________________#

        #Filtra a tabela de zoneamento e uso

        nome_coluna = df_cnaes_risco_uso_selecionado[id_uso].name
        df_usoselect = pd.merge(df_zona_col, df_cnaes_risco_uso_selecionado[id_uso], left_on='ZONA',right_on=nome_coluna, how='inner')
        filtro_colunas = df_usoselect['COL'].unique().tolist()
        filtro_colunas.insert(0,0)
        df_usoselect_filtrado = df_risco_uso.iloc[:, filtro_colunas]
        df_usoselect_filtrado = df_usoselect_filtrado.loc[df_usoselect_filtrado['ZONA'] == zon_regin]
        
     

#______________________________________________________________________________________________#


        #Printa as verificações com o streamlit
        #Resumo do processo
        st.divider()
        st.subheader('Resumo do processo')
        st.markdown('Razão Social: '+razao_social_regin)
        st.markdown('CNPJ: '+cnpj_regin[0])
        st.markdown('Área construída: '+str(area_construida_regin)+' m²')

        #Análise de risco
        st.subheader('Classificação de risco e uso das atividades')
        st.dataframe(df_cnaes_risco_uso_selecionado, hide_index=True)

        #Localização
        st.subheader('Localização')
        st.markdown('Endereço no REGIN: '+logradouro_regin+' '+numero_predial_regin+', '+bairro_regin)
        st.markdown('Complemento no REGIN: ')
        st.markdown('Inscrição Imobiliária:'+' '+inscr_regin)
        st.markdown('Consulta prévia:  https://arcgis.itajai.sc.gov.br/geoitajai/plantacadastral/consultaprevia.html#i'+inscr_arcgis)
        st.markdown('Planta de situação: https://arcgis.itajai.sc.gov.br/geoitajai/plantacadastral/plantalocalizacao.html#i'+inscr_arcgis)
        #st.markdown('Google maps: '+str('https://www.google.com/maps/place/')+logradouro_regin+str(numero_predial_regin)+str('+Itajai+-+SC'))


        #Permissão de uso
        st.subheader('Permisão de uso')
        st.markdown('Zoneamento: '+zon_regin)
        st.markdown('Classificação de uso: '+class_uso)     
        st.dataframe(df_usoselect_filtrado, hide_index=True) 
     

except:
    st.markdown(''':red[Verifique o correto preenchimento de todos os campos.]''')
