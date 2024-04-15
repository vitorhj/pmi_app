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
st.sidebar.page_link("pages/lista-escritorios-virtuais.py", label="")


#Página principal do Streamlit - fixa

st.image(logo_image, width=150)
st.subheader('Lista de escritórios virtuais - ALF')

#Tabelas CSV

df_ev=pd.read_csv("escritorios-virtuais.csv", nrows=2000)
st.dataframe(df_ev, hide_index=True)
