import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_file import load_dataset
from utils.ui import setup_sidebar, add_back_to_top
from utils.visualizations import plot_bar, plot_boxplot, plot_histogram

st.set_page_config(page_title="Segmentação RFM", page_icon="👥", layout="wide")

setup_sidebar()
add_back_to_top()

st.title("👥 Segmentação de Clientes com RFM")


# --- Constants ---
MONETARY_COLS = [
    "total_vinho",
    "total_frutas",
    "total_carnes",
    "total_peixes",
    "total_doces",
    "total_outros",
]

# Order for visualization (Best to Worst)
SEGMENT_ORDER = [
    "Campeões",
    "Leais",
    "Potenciais Leais",
    "Novos",
    "Promissores",
    "Precisam de Atenção",
    "Em Risco",
    "Hibernando",
]

# Consistent Colors for Segments
SEGMENT_COLORS = {
    "Campeões": "#28A745",  # Green
    "Leais": "#20C997",  # Teal
    "Potenciais Leais": "#17A2B8",  # Cyan
    "Novos": "#007BFF",  # Blue
    "Promissores": "#6f42c1",  # Purple
    "Precisam de Atenção": "#fd7e14",  # Orange
    "Em Risco": "#dc3545",  # Red
    "Hibernando": "#6c757d",  # Gray/Dark
}


# --- Data Loading ---
@st.cache_data
def load_and_merge_data():
    try:
        df_clientes = load_dataset("mercado_clientes_pt.xlsx")
        df_resumo = load_dataset("mercado_resumo_compras_pt.xlsx")
        df_transacoes = load_dataset("mercado_transacoes_pt.xlsx")

        df = pd.merge(df_clientes, df_resumo, on="id_cliente", how="left")

        return df, df_transacoes, df_clientes, df_resumo
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None


df, df_transacoes, df_clientes, df_resumo = load_and_merge_data()


def get_segment(r, f):
    # Expanded logic to address feedback about unbalanced "Regular" group
    # 5 is Best (Recent, High Freq)
    if r >= 5 and f >= 5:
        return "Campeões"
    elif r >= 4 and f >= 4:
        return "Leais"
    elif r >= 4 and f >= 2:
        return "Potenciais Leais"
    elif r >= 4 and f <= 1:
        return "Novos"
    elif r >= 3 and f >= 3:
        return "Promissores"
    elif r >= 3 and f <= 2:
        return "Precisam de Atenção"
    elif r >= 2 and f >= 2:
        return "Em Risco"
    else:
        return "Hibernando"


@st.cache_data
def generate_rfm_data(df_transacoes, df_merged):
    # --- Pre-processing Transações ---
    # Ensure dates
    if "data_transacao" in df_transacoes.columns:
        df_transacoes["data_transacao"] = pd.to_datetime(
            df_transacoes["data_transacao"]
        )

    # 1. Calculate Recency & Frequency (from Transactions)
    reference_date = df_transacoes["data_transacao"].max() + pd.Timedelta(days=1)

    rf_metrics = (
        df_transacoes.groupby("id_cliente")
        .agg(
            {
                "data_transacao": lambda x: (reference_date - x.max()).days,
                "id_transacao": "count",
            }
        )
        .reset_index()
    )

    rf_metrics.columns = ["id_cliente", "Recency", "Frequency"]

    # 2. Calculate Monetary (from Merged Summary Data)
    # Check if columns exist in df_merged, default to 0 if not
    for col in MONETARY_COLS:
        if col not in df_merged.columns:
            df_merged[col] = 0

    df_merged["Monetary"] = df_merged[MONETARY_COLS].sum(axis=1)

    # 3. Merge R, F, M
    # Use inner merge to only score customers who have transactions AND summary data
    # Or left merge to keep all transaction customers?
    # Usually we want RFM for active customers.
    rfm = pd.merge(
        rf_metrics, df_merged[["id_cliente", "Monetary"]], on="id_cliente", how="left"
    )
    rfm["Monetary"] = rfm["Monetary"].fillna(0)

    # --- Scoring (Quintiles 1-5) ---
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    )
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str)

    # --- Segment Map ---
    rfm["Segment"] = rfm.apply(
        lambda row: get_segment(int(row["R_Score"]), int(row["F_Score"])), axis=1
    )

    return rfm


# --- Tabs ---
tab_overview, tab_rfm, tab_analysis, tab_results = st.tabs(
    ["Visão Geral", "Segmentação RFM", "Análise Detalhada", "Conclusões e Insights"]
)

with tab_overview:
    st.markdown(
        """
        O Mercado atua em um setor altamente competitivo e enfrenta mudanças no comportamento dos consumidores. A fidelização de clientes tem se tornado cada vez mais desafiadora.
        Para manter e aumentar a receita, buscamos entender melhor a base de clientes e personalizar estratégias de marketing e retenção.
        Nossa solução é baseada na aplicação da metodologia RFM para segmentar clientes com base em seu comportamento de compra; e da lei de pareto para entender quem são nossos clientes que representam 20% do nosso rendimento.
    """
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Clientes", df.shape[0])
    col2.metric("Clientes com Transações", df_transacoes["id_cliente"].nunique())

    total_sales = 0
    available_cols = [c for c in MONETARY_COLS if c in df.columns]
    if available_cols:
        total_sales = df[available_cols].sum().sum()

    col3.metric("Total de Vendas", f"R$ {total_sales:,.2f}")

    st.subheader("Estrutura dos Arquivos")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Clientes**")
        st.write(list(df_clientes.columns))

    with col_b:
        st.markdown("**Resumo de Compras**")
        st.write(list(df_resumo.columns))

    with col_c:
        st.markdown("**Transações**")
        st.write(list(df_transacoes.columns))

    st.subheader("Amostra dos Dados Unificados")
    st.dataframe(df.head(), use_container_width=True)

with tab_rfm:
    st.header("Análise RFM (Recência, Frequência, Valor)")
    st.expander("Metodologia RFM", expanded=False).markdown(
        """
    **Metodologia:**
    - **Recência (R)**: Dias desde a última compra.
    - **Frequência (F)**: Quantidade de compras/transações.
    - **Valor (M)**: Valor total gasto.
    """
    )

    rfm = generate_rfm_data(df_transacoes, df)

    st.subheader("Distribuição dos Segmentos")

    rfm_full = pd.merge(
        rfm,
        df[["id_cliente", "ano_nascimento", "estado_civil"]],
        on="id_cliente",
        how="left",
    )

    # Bar Chart of Segments
    seg_counts = rfm["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]

    seg_counts["Segment"] = pd.Categorical(
        seg_counts["Segment"], categories=SEGMENT_ORDER, ordered=True
    )
    seg_counts = seg_counts.sort_values("Segment", ascending=True)

    plot_bar(
        seg_counts,
        x_col="Count",
        y_col="Segment",
        orientation="h",
        title="Contagem de Clientes por Segmento",
        color="Segment",
        labels={"Count": "Quantidade", "Segment": "Segmento"},
        show_legend=False,
        height=450,
        color_map=SEGMENT_COLORS,
    )

    st.subheader("Matriz RF (Recência x Frequência)")
    fig_scatter = px.scatter(
        rfm,
        x="Recency",
        y="Frequency",
        color="Segment",
        size="Monetary",
        hover_data=["id_cliente"],
        title="Matriz RF (Tamanho = Valor Monetário)",
        color_discrete_map=SEGMENT_COLORS,
        labels={"Recency": "Recência (Dias)", "Frequency": "Frequência (Vezes)"},
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Detalhes dos Grupos")

    # Group metrics by Segment
    rfm_summary = (
        rfm.groupby("Segment")[["Recency", "Frequency", "Monetary"]]
        .mean()
        .reset_index()
    )

    # Add Count of customers per segment
    counts = rfm["Segment"].value_counts().reset_index()
    counts.columns = ["Segment", "Count"]
    rfm_summary = rfm_summary.merge(counts, on="Segment")

    # Order by Segment Quality
    rfm_summary["Segment"] = pd.Categorical(
        rfm_summary["Segment"], categories=SEGMENT_ORDER, ordered=True
    )
    rfm_summary = rfm_summary.sort_values("Segment")

    # Renaming for display
    rfm_summary.columns = [
        "Segmento",
        "Recência Média (Dias)",
        "Frequência Média",
        "Valor Monetário Médio (R$)",
        "Qtd Clientes",
    ]

    st.dataframe(
        rfm_summary.style.format(
            {
                "Recência Média (Dias)": "{:.1f}",
                "Frequência Média": "{:.1f}",
                "Valor Monetário Médio (R$)": "R$ {:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

with tab_analysis:
    st.header("Análise Detalhada dos Segmentos")

    plot_boxplot(
        rfm,
        x="Segment",
        y="Recency",
        color="Segment",
        title="Distribuição de Recência por Segmento",
        color_map=SEGMENT_COLORS,
        labels={"Recency": "Recência (Dias)", "Segment": "Segmento"},
    )

    plot_boxplot(
        rfm,
        x="Segment",
        y="Frequency",
        color="Segment",
        title="Distribuição de Frequência por Segmento",
        color_map=SEGMENT_COLORS,
        labels={"Frequency": "Frequência (Vezes)", "Segment": "Segmento"},
    )

    plot_boxplot(
        rfm,
        x="Segment",
        y="Monetary",
        color="Segment",
        title="Distribuição de Valor Monetário por Segmento",
        color_map=SEGMENT_COLORS,
        labels={"Monetary": "Valor Monetário (R$)", "Segment": "Segmento"},
    )

    # Histogram of Monetary Value (Log scale maybe?)
    st.subheader("Distribuição de Valor Monetário (Geral)")
    plot_histogram(
        rfm,
        x="Monetary",
        title="Histograma de Valor Monetário",
        labels={"Monetary": "Valor Monetário (R$)", "count": "Quantidade"},
        color_map=SEGMENT_COLORS,
    )


with tab_results:
    st.header("Conclusões e Insights Estratégicos")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### Perfil do Cliente")
            st.markdown(
                """
            - **Escolaridade**: 50.3% Ensino Superior, 38.2% Pós-graduação.
            - **Renda**: 60.7% Classe Média.
            - **Família**: Média de 1 filho.
            - **Público de Ouro**: Casados de meia-idade (maior volume de compras e frequência).
            """
            )

        with st.container(border=True):
            st.markdown("#### Comportamento de Compra")
            st.markdown(
                """
            - **Frequência**: 43.5% compram a cada 30-60 dias (Frequência Média).
            - **Ticket**: Gasto polarizado entre \\$20 (básico) e >\\$75 (Alto Valor - 25% da base).
            - **Crescimento**: Salto de +447% nas vendas de 2020 para 2021.
            """
            )

    with col2:
        with st.container(border=True):
            st.markdown("#### Demografia")
            st.markdown(
                """
            - **Idade**: 43.4% são de Meia-idade.
            - **Jovens**: Apenas 1.9% da base.
            - **Estado Civil**: Bem distribuído (58% em União Estável/Solteiros/Divorciados).
            """
            )

        with st.container(border=True):
            st.markdown("#### Produtos e Receita")
            st.markdown(
                """
            - **Carro-chefe**: Vinho (50.2% do faturamento).
            - **Canais**: Vendas bem distribuídas entre Loja Física e Online.
            """
            )

    st.subheader("Estratégias Recomendadas")
    st.info("Estratégias baseadas nos 8 grupos da nova segmentação.")

    st.markdown(
        """
    1. **Campeões e Leais (Manter e Recompensar)**:
    - **Ação**: Tratamento VIP, acesso antecipado a lançamentos e produtos exclusivos.
    - **Objetivo**: Manter o engajamento alto e transformar em defensores da marca.

    2. **Potenciais Leais e Novos (Crescer)**:
    - **Ação**: Ofertas de "segunda compra", convite para programa de fidelidade e onboarding.
    - **Objetivo**: Aumentar a frequência e criar hábito de compra.

    3. **Promissores e Precisam de Atenção (Reter)**:
    - **Ação**: Recomendações personalizadas (Cross-sell) e ofertas por tempo limitado.
    - **Objetivo**: Evitar que a recência aumente e trazê-los de volta à loja.

    4. **Em Risco e Hibernando (Recuperar)**:
    - **Ação**: Campanhas de "Sua falta foi notada" com descontos agressivos em produtos âncora.
    - **Objetivo**: Reativação rápida antes do churn definitivo.
    """
    )
