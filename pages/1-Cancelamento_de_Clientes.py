import streamlit as st
from utils.load_file import load_dataset
from utils.ui import setup_sidebar, add_back_to_top
from utils.visualizations import (
    plot_pie,
    plot_histogram,
    plot_boxplot,
    plot_heatmap,
    show_grouped_metrics,
    show_univariate_grid,
    show_bivariate_grid,
)

st.set_page_config(
    page_title="Análise de Cartão de Crédito", page_icon="💳", layout="wide"
)
setup_sidebar()
add_back_to_top()

st.title("💳 Análise de Cancelamento de Cartão de Crédito")

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
            "Visão Geral",
            "Metodologia de Limpeza",
            "Métricas",
            "Análise Univariada",
            "Análise de Correlação",
            "Análise Bivariada",
        ]
    )
)

with tab_overview:
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
        plot_pie(df, names="Categoria", height=350)

    metrics_groups = {
        "Informação da Pessoa": [
            "Idade",
            "Sexo",
            "Dependentes",
            "Educação",
            "Estado Civil",
            "Faixa Salarial Anual",
        ],
        "Relacionamento com o Banco": [
            "Categoria Cartão",
            "Meses como Cliente",
            "Produtos Contratados",
            "Inatividade 12m",
            "Contatos 12m",
            "Limite",
            "Limite Consumido",
            "Limite Disponível",
        ],
        "Alterações de Consumo": [
            "Mudanças Transacoes_Q4_Q1",
            "Valor Transacoes 12m",
            "Qtde Transacoes 12m",
            "Mudança Qtde Transações_Q4_Q1",
            "Taxa de Utilização Cartão",
        ],
    }
    show_grouped_metrics(df, metrics_groups)


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

    plot_histogram(df, x=selected_col, color="Categoria", title=title)

    show_univariate_grid(df, numeric_cols, categorical_cols)

with tab_heat_map:
    st.header("Mapa de Calor de Correlação")
    plot_heatmap(df, numeric_cols)

with tab_bivariate:
    st.header("Análise Bivariada (Boxplots)")
    y_col = st.selectbox(
        "Selecione a variável numérica para comparar com Churn:", numeric_cols, index=0
    )
    plot_boxplot(
        df,
        x="Categoria",
        y=y_col,
        color="Categoria",
        title=f"{y_col} vs Status de Churn",
    )

    show_bivariate_grid(df, numeric_cols)
