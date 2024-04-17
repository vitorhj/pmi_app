import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import re
from itertools import chain

#Configurações do Streamlit

st.set_page_config(page_title='Links úteis', 
                   layout="centered", 
                   initial_sidebar_state='expanded',
                   menu_items=None
                   )



#Sidebar
st.sidebar.page_link("viabilidade_empresas.py", label="")
st.sidebar.page_link("pages/verifica_aprova.py", label="")
st.sidebar.page_link("pages/links.py", label="")


#Página principal do Streamlit - fixa
st.image(logo_image, width=150)
st.subheader('Links úteis')
st.markdown('CNPJ: '+str('https://servicos.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp'))
st.markdown('REGIN: '+str('http://regin.jucesc.sc.gov.br/regin.externo/CON_ViabilidadeSelecaoExternoV4.aspx?'))
st.markdown('GEO: '+str('https://arcgis.itajai.sc.gov.br/geoitajai/plantacadastral/plantacadastral.html'))
st.markdown('CBMSC: '+str('https://esci.cbm.sc.gov.br/Safe/PublicoExterno/ControllerConferenciaDigital/'))
st.markdown('PMI ALVARÁ: '+str('https://portaldocidadao.itajai.sc.gov.br/servico_link/7'))
st.markdown('PMI TERMO ÚNICO: '+str('https://portaldocidadao.itajai.sc.gov.br/servico.php?id=89'))
st.markdown('ALVARÁ PROVISÓRIO: '+str('https://portaldocidadao.itajai.sc.gov.br/c/88'))
st.markdown('DRIVE: '+str('https://drive.google.com/drive/folders/1LfDRxkb8Tv6fspqjBGuToB0xAQO-xGDv?usp=sharing'))
st.markdown('MAPA SETORES: '+str('https://arcgis.itajai.sc.gov.br/portal/apps/webappviewer/index.html?id=ab4e19d77cc547968dce80dce054d8db'))
st.markdown('ESCRITÓRIOS VIRTUAIS: '+str('https://docs.google.com/spreadsheets/d/1J0gHPYf69kp0F9flnAQBqPf8rQ0ScrUVoHN7vxEij30/edit?usp=sharing'))
