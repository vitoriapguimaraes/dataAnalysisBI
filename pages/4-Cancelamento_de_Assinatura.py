import streamlit as st
import pandas as pd
from utils.load_file import load_dataset
from utils.ui import setup_sidebar, add_back_to_top
from utils.visualizations import plot_bar

st.set_page_config(
    page_title="Cancelamento de Assinaturas", page_icon="🔄", layout="wide"
)

setup_sidebar()
add_back_to_top()

st.title("🔄 Análise de Cancelamento de Assinaturas")

# Data Loading
try:
    df_raw = load_dataset("cancelamentos_servico.csv")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# --- Pre-processing ---
df = df_raw.copy()

cols_to_drop = ["Unnamed: 0", "Codigo"]
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors="ignore")

rows_before = len(df)
df = df.dropna()
rows_after = len(df)

if "Aposentado" in df.columns:
    df["Aposentado"] = (
        df["Aposentado"].astype(int).astype(str).map({"0": "Não", "1": "Sim"})
    )

    df["TotalGasto"] = pd.to_numeric(df["TotalGasto"], errors="coerce")
    df = df.dropna(subset=["TotalGasto"])

if df["Churn"].dtype == "object":
    df["Churn_Bin"] = df["Churn"].map({"Sim": 1, "Nao": 0})
else:
    df["Churn_Bin"] = df["Churn"]

# --- Tabs ---
tab_overview, tab_clean, tab_analysis, tab_insights = st.tabs(
    [
        "Visão Geral",
        "Metodologia de Limpeza",
        "Análise de Cancelamento",
        "Insights & Solução",
    ]
)

with tab_overview:
    st.markdown(
        """
        A perda de clientes (Churn) é um dos maiores desafios para empresas de receita recorrente. Neste estudo de caso, analisamos os dados de uma operadora de Telecom para identificar padrões de comportamento de clientes que cancelaram o serviço.

        O projeto tem como objetivos diagnosticar a taxa de cancelamento global e por segmentos, identificar as variáveis que mais influenciam a decisão de saída (como contrato e suporte) e propor um plano de ação estratégico para reduzir o churn e aumentar o Life Time Value (LTV).
        """
    )

    # Key Metrics
    col1, col2, col3 = st.columns(3)
    total_customers = len(df)
    churn_count = df["Churn_Bin"].sum()
    churn_rate = churn_count / total_customers

    col1.metric("Total de Clientes", total_customers)
    col2.metric("Cancelamentos", int(churn_count))
    col3.metric("Taxa de Churn Global", f"{churn_rate:.1%}", delta_color="inverse")

    st.markdown("---")
    st.subheader("Amostra dos Dados")
    st.dataframe(df.head(), use_container_width=True)


with tab_clean:
    st.header("Processo de Limpeza de Dados")
    st.markdown(
        """
        Para garantir a consistência da análise, foram aplicadas as seguintes etapas de pré-processamento:
        1. **Remoção de Colunas**:
           - `Unnamed: 0`, `Codigo`: Índices e identificadores irrelevantes para modelos preditivos/analíticos.
        2. **Tratamento de Dados Faltantes**:
           - Linhas com valores nulos foram removidas para evitar distorções.
        3. **Conversão de Tipos**:
           - `TotalGasto`: Convertido de texto para numérico.
           - `Aposentado`: Ajustado de numérico para Categórico (Sim/Não).
        4. **Mapeamento de Target**:
           - A coluna `Churn` foi binarizada (Sim=1, Não=0) para facilitar cálculos de taxa.
        """
    )

    st.code(
        """
# Exemplo do pipeline de limpeza:
cols_to_drop = ["Unnamed: 0", "Codigo"]
df = df.drop(columns=cols_to_drop, errors="ignore")

# Remoção de Nulos e Conversão
df = df.dropna()
df["TotalGasto"] = pd.to_numeric(df["TotalGasto"], errors="coerce")
df["Aposentado"] = df["Aposentado"].astype(int).map({0: "Não", 1: "Sim"})

# Target Binário
df["Churn_Bin"] = df["Churn"].map({"Sim": 1, "Nao": 0})
        """,
        language="python",
    )

    if rows_before != rows_after:
        st.info(
            f"ℹ️ **Status da Limpeza**: {rows_before - rows_after} linhas foram removidas por conterem valores nulos."
        )

with tab_analysis:
    st.header("Exploração dos Fatores de Cancelamento")

    churn_by_contract = df.groupby("TipoContrato")["Churn_Bin"].mean().reset_index()
    churn_by_contract["Churn Rate"] = churn_by_contract["Churn_Bin"]
    churn_by_contract = churn_by_contract.sort_values("Churn Rate", ascending=False)

    col_plot, col_info = st.columns([2, 1])

    with col_plot:
        plot_bar(
            churn_by_contract,
            x_col="TipoContrato",
            y_col="Churn Rate",
            title="Taxa de Cancelamento por Tipo de Contrato",
            labels={
                "Churn Rate": "Taxa de Cancelamento",
                "TipoContrato": "Contrato",
            },
            color="TipoContrato",
            show_legend=False,
        )
    with col_info:
        st.info(
            """
            **Observação Crítica:**
            Contratos **Mensais** apresentam uma taxa de cancelamento drasticamente superior aos anuais.
            """
        )

    explore_cols = [
        c
        for c in df.columns
        if c
        not in [
            "IDCliente",
            "Churn",
            "Churn_Bin",
            "TotalGasto",
            "ValorMensal",
            "TipoContrato",
        ]
    ]

    # Separar por cardinalidade
    # Binárias (até 2 valores únicos) -> 3 colunas (Grid menor)
    cols_binary = [c for c in explore_cols if df[c].nunique() <= 2]
    # Múltiplas Categorias (> 2 valores) -> 2 colunas (Grid maior)
    cols_multi = [c for c in explore_cols if df[c].nunique() > 2]

    with st.container(border=True):

        st.markdown("### Todos os Fatores")

        if cols_multi:
            cols2 = st.columns(2)
            for i, selected_var in enumerate(cols_multi):
                with cols2[i % 2]:
                    churn_by_var = (
                        df.groupby(selected_var)["Churn_Bin"].mean().reset_index()
                    )
                    churn_by_var = churn_by_var.sort_values(
                        "Churn_Bin", ascending=False
                    )

                    plot_bar(
                        churn_by_var,
                        x_col=selected_var,
                        y_col="Churn_Bin",
                        title=f"{selected_var}",
                        labels={"Churn_Bin": "Taxa", selected_var: ""},
                        color=selected_var,
                        height=300,
                        show_legend=False,
                    )

        if cols_binary:
            cols3 = st.columns(3)
            for i, selected_var in enumerate(cols_binary):
                with cols3[i % 3]:
                    churn_by_var = (
                        df.groupby(selected_var)["Churn_Bin"].mean().reset_index()
                    )
                    churn_by_var = churn_by_var.sort_values(
                        "Churn_Bin", ascending=False
                    )

                    plot_bar(
                        churn_by_var,
                        x_col=selected_var,
                        y_col="Churn_Bin",
                        title=f"{selected_var}",
                        labels={"Churn_Bin": "Taxa", selected_var: ""},
                        color=selected_var,
                        height=250,
                        show_legend=False,
                    )

with tab_insights:
    st.header("Diagnóstico e Plano de Ação")

    col1_choice, col2_result = st.columns(2)

    with col1_choice:
        st.subheader("Simulação de Cenário")
        st.markdown(
            "O que acontece com a taxa de Churn se removermos os contratos mensais problemáticos?"
        )
        remove_monthly = st.checkbox("Simular exclusão do contrato 'Mensal'")

    with col2_result:

        if remove_monthly:
            df_sim = df[df["TipoContrato"] != "Mensal"]
            new_churn = df_sim["Churn_Bin"].mean()
            improvement = churn_rate - new_churn

            c1, c2 = st.columns(2)
            c1.metric("Nova Taxa de Churn", f"{new_churn:.1%}")
            c2.metric("Redução Alcançada", f"-{improvement:.1%}", delta="Positivo")

            st.success(
                "A remoção de contratos mensais derruba drasticamente o cancelamento!"
            )
        else:
            st.metric("Taxa Atual", f"{churn_rate:.1%}")

    st.subheader("Recomendações Estratégicas")
    st.markdown(
        """
        1. **Incentivar Planos Anuais**:
            - Criar descontos agressivos para migração de Mensal -> Anual.
            - O contrato mensal é a principal porta de saída.
        2. **Atenção ao Call Center**:
            - Clientes com muitas ligações (CallCenter) têm alto risco. Implementar "Sinal Vermelho" no CRM para atendimento prioritário.
        3. **Atrasos de Pagamento**:
            - Implementar régua de cobrança preventiva para evitar bloqueios que gerem insatisfação e cancelamento.
        """
    )
