import streamlit as st

from utils.ui import setup_sidebar, add_back_to_top

st.set_page_config(page_title="Análise de Dados e BI", page_icon="📊", layout="wide")

add_back_to_top()

st.title("Análise de Dados e Business Intelligence")

st.code(
    "Acesse a Análise Exploratória de Dados, seguida pela Visualizações, Métricas e Insights, na lista abaixo ou na barra lateral"
)

st.page_link(
    "pages/1-Cancelamento_de_Clientes.py",
    label="Análise de Cancelamento de Cartão de Crédito",
    icon="💳",
    use_container_width=True,
)

st.page_link(
    "pages/2-Varejo.py",
    label="Análise de Dados de Varejo",
    icon="🛍️",
    use_container_width=True,
)

st.markdown("---")

st.subheader("Ferramentas utilizadas")
st.code("Streamlit | Pandas | Matplotlib | Seaborn | Plotly")

setup_sidebar()
