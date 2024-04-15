import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import re
import os
from itertools import chain

#Configurações do Streamlit

st.set_page_config(page_title='App', 
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
st.sidebar.page_link("pages/estudo-de-impacto-de-vizinhanca.py", label="")


#Página principal do Streamlit - fixa

st.image(logo_image, width=150)
st.subheader('Estudo de Impacto de Vizinhança - EIV')

col1, col2 = st.columns(2)

with col1:
    ib_zon = st.text_input(
    "Inscrição Imobiliária (Padrão 000.000.00.0000)",
    key="ib_iscricao"
    )

with col2:
    ib_area = st.number_input(
    "Área cosntruída (m²)",
    key="ib_area"
    )

ib_tipo = st.text_input(
    "Tipo de empreendimento ou Atividade",
    key="ib_cnpj"
    )

def clear_text():
    st.session_state["ib_tipo"] = ""
    st.session_state["ib_area"] = 0
    st.session_state["ib_zon"] = ""
st.button("Limpar", on_click=clear_text)

st.divider()    
