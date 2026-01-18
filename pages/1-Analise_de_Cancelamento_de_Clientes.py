import streamlit as st
import plotly.express as px
from utils.load_file import load_dataset

from utils.ui import setup_sidebar

st.set_page_config(
    page_title="Análise de Cartão de Crédito", page_icon="📊", layout="wide"
)
setup_sidebar()

st.title("Análise de Cancelamento de Cartão de Crédito")

# Data Loading
try:
    df = load_dataset("bank_credit_card_cancellation.csv")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Cleaning
cols_to_drop = ["CLIENTNUM"] + [c for c in df.columns if "Naive_Bayes" in c]
df = df.drop(columns=cols_to_drop, errors="ignore")

# Tabs
tab_overview, tab_clean, tab_metrics, tab_univariate, tab_heat_map, tab_bivariate = (
    st.tabs(
        [
            "Visão Geral do Dataset",
            "Metodologia de Limpeza",
            "Métricas",
            "Análise Univariada",
            "Análise de Correlação",
            "Análise Bivariada",
        ]
    )
)

with tab_overview:
    st.subheader("Sobre o Dataset")
    st.markdown(
        "Este conjunto de dados contém informações sobre clientes de cartão de crédito e se eles cancelaram ou não."
    )
    st.dataframe(df.head())

    st.subheader("Principais Insights e Hipóteses")
    st.markdown(
        """
    Com base na análise exploratória, identificamos os seguintes comportamentos nos clientes que cancelam (Churn):
    1.  **Baixa Utilização do Cartão**: Clientes com **menos transações (`Total_Trans_Amt`)** ou **menor saldo rotativo (`Total_Revolving_Bal`)** tendem a cancelar mais. Isso indica que clientes que não engajam com o produto acabam saindo.
    2.  **Alto Número de Contatos**: Clientes cancelados **entram em contato com o banco muito mais vezes (`Contacts_Count_12_mon`)** antes de sair, sugerindo frustração ou problemas não resolvidos.
    3.  **Inatividade**: Clientes com maior tempo de inatividade (`Months_Inactive_12_mon`) também apresentam risco elevado.

    **Conclusão preliminar**: O cancelamento parece estar ligado fortemente ao **desengajamento** (não uso do produto) e **insatisfação** (muitos contatos com suporte).
    """
    )


with tab_clean:
    st.header("Processo de Limpeza de Dados")
    st.markdown(
        """
    Para garantir a qualidade da análise, foram realizadas as seguintes etapas de pré-processamento:
    1. **Remoção de Colunas Irrelevantes**:
       - `CLIENTNUM`: Identificador único do cliente, sem valor estatístico.
       - Colunas `Naive_Bayes`: Artefatos presentes no dataset original que não devem ser usados.
    2. **Tratamento de Dados**:
       - Identificação e compatibilização dos nomes das colunas (Português/Inglês).
    """
    )

    st.code(
        """
# Exemplo do código de limpeza utilizado:
cols_to_drop = ['CLIENTNUM'] + [c for c in df.columns if 'Naive_Bayes' in c]
df = df.drop(columns=cols_to_drop, errors='ignore')
    """,
        language="python",
    )

with tab_metrics:
    col1, col2 = st.columns(2)
    col1.header("Métricas")
    col1.metric("Total Clientes", df.shape[0])
    col1.metric("Total Colunas", df.shape[1])
    with col2:
        fig = px.pie(df, names="Categoria")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Estatísticas Descritivas por Grupo")

    with st.container(border=True):
        st.markdown("Informação da Pessoa")
        cols_pessoa = [
            "Idade",
            "Sexo",
            "Dependentes",
            "Educação",
            "Estado Civil",
            "Faixa Salarial Anual",
        ]
        available_cols = [c for c in cols_pessoa if c in df.columns]
        st.dataframe(
            df[available_cols].describe(include="all"), use_container_width=True
        )

    with st.container(border=True):
        st.markdown("Relacionamento com o Banco")
        cols_cliente = [
            "Categoria Cartão",
            "Meses como Cliente",
            "Produtos Contratados",
            "Inatividade 12m",
            "Contatos 12m",
            "Limite",
            "Limite Consumido",
            "Limite Disponível",
        ]
        available_cols = [c for c in cols_cliente if c in df.columns]
        st.dataframe(
            df[available_cols].describe(include="all"), use_container_width=True
        )

    with st.container(border=True):
        st.markdown("Alterações de Consumo")
        cols_consumo = [
            "Mudanças Transacoes_Q4_Q1",
            "Valor Transacoes 12m",
            "Qtde Transacoes 12m",
            "Mudança Qtde Transações_Q4_Q1",
            "Taxa de Utilização Cartão",
        ]
        available_cols = [c for c in cols_consumo if c in df.columns]
        st.dataframe(
            df[available_cols].describe(include="all"), use_container_width=True
        )


with tab_univariate:
    st.header("Análise Univariada")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    col1, col2 = st.columns(2)
    with col1:
        col_type = st.radio(
            "Selecione o tipo de variável:", ["Numérica", "Categórica"], horizontal=True
        )
    with col2:
        if col_type == "Numérica":
            selected_col = st.selectbox("Selecione a coluna:", numeric_cols)
            title = f"Distribuição de {selected_col}"
        else:
            selected_col = st.selectbox("Selecione a coluna:", categorical_cols)
        title = f"Distribuição de {selected_col}"

    fig = px.histogram(
        df, x=selected_col, color="Categoria", title=title, barmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Todas as distribuições")
        all_cols = numeric_cols + categorical_cols

        if "Categoria" in all_cols:
            all_cols.remove("Categoria")

        cols = st.columns(3)
        for i, col in enumerate(all_cols):
            with cols[i % 3]:
                fig_all = px.histogram(
                    df, x=col, color="Categoria", title=col, barmode="group"
                )
                fig_all.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0),
                    yaxis_title=None,
                )
                st.plotly_chart(fig_all, use_container_width=True)

with tab_heat_map:
    st.header("Mapa de Calor de Correlação")
    corr = df[numeric_cols].corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        origin="lower",
    )
    fig_corr.update_layout(height=600)
    st.plotly_chart(fig_corr, use_container_width=True)

with tab_bivariate:
    st.header("Análise Bivariada (Boxplots)")
    y_col = st.selectbox(
        "Selecione a variável numérica para comparar com Churn:", numeric_cols, index=0
    )
    fig_box = px.box(
        df,
        x="Categoria",
        y=y_col,
        color="Categoria",
        title=f"{y_col} vs Status de Churn",
    )
    st.plotly_chart(fig_box, use_container_width=True)

    with st.container(border=True):
        st.subheader("Todas as Análises Bivariadas")
        cols = st.columns(3)
        for i, col in enumerate(numeric_cols):
            with cols[i % 3]:
                fig_all = px.box(
                    df, x="Categoria", y=col, color="Categoria", title=f"{col} vs Churn"
                )
                fig_all.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0),
                    xaxis_title=None,
                )
                st.plotly_chart(fig_all, use_container_width=True)
