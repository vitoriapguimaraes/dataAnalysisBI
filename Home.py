import streamlit as st

from utils.ui import setup_sidebar

st.set_page_config(page_title="Análise de Dados e BI", page_icon="📊", layout="wide")

st.title("Análise de Dados e Business Intelligence")

st.code(
    "Acesse a AED do dataset, seguida pela análise e visualizações, na lista abaixo ou na barra lateral"
)

st.page_link(
    "pages/1-Analise_de_Cancelamento_de_Clientes.py",
    label="Análise de Cancelamento de Cartão de Crédito",
)

st.markdown("---")

st.subheader("Ferramentas utilizadas")
st.code("Streamlit | Pandas | Matplotlib | Seaborn | Plotly")

setup_sidebar()
