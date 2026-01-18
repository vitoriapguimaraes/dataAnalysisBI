import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.load_file import load_dataset
from utils.ui import setup_sidebar, add_back_to_top
from utils.visualizations import (
    show_univariate_grid,
    plot_histogram,
    plot_bar,
    COLOR_PALETTE,
)

st.set_page_config(page_title="Análise de Varejo", page_icon="🛍️", layout="wide")

setup_sidebar()
add_back_to_top()

st.title("🛍️ Análise de Dados de Varejo")

# Data Loading
try:
    df = load_dataset("retail.csv")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# --- Pré-processamento ---
# Converter datas
if "Data_Pedido" in df.columns:
    df["Data_Pedido"] = pd.to_datetime(
        df["Data_Pedido"], dayfirst=True, errors="coerce"
    )
    df["Ano"] = df["Data_Pedido"].dt.year
    df["Mes"] = df["Data_Pedido"].dt.month
    df["Ano_Mes"] = df["Data_Pedido"].dt.strftime("%Y/%m")

# Garantir tipos numéricos
numeric_cols = ["Valor_Venda"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Colunas categóricas de interesse
categorical_cols = ["Segmento", "Pais", "Cidade", "Estado", "Categoria", "SubCategoria"]

# Tabs
tab_overview, tab_univariate, tab_qa = st.tabs(
    ["Visão Geral", "Análise Univariada", "Respostas de Negócio"]
)

with tab_overview:

    # Sobre o dataset
    st.markdown(
        """
        Este conjunto de dados apresenta um panorama detalhado das operações de vendas de uma grande rede varejista.A análise abrange métricas de desempenho financeiro, distribuição geográfica e comportamento por segmentos, permitindo identificar oportunidades de otimização de receita e eficiência nas estratégias de descontos.
        """
    )

    # Métricas Principais
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    col1.metric("Total de Vendas", f"R$ {df['Valor_Venda'].sum():,.2f}")
    col2.metric("Total de Pedidos", df.shape[0])
    col3.metric("Clientes Únicos", df["ID_Cliente"].nunique())
    col4.metric("Cidades Atendidas", df["Cidade"].nunique())

    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Informações Estatísticas")
    st.dataframe(df.describe(), use_container_width=True)

with tab_univariate:
    st.header("Análise Univariada")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    # Excluir colunas de ID
    categorical_cols = [col for col in categorical_cols if "ID" not in col]

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

    # Filtra colunas que realmente existem
    valid_num = [c for c in numeric_cols if c in df.columns]
    valid_cat = [c for c in categorical_cols if c in df.columns]

    show_univariate_grid(df, valid_num, valid_cat)

with tab_qa:
    st.header("Perguntas de Negócio")
    st.markdown("Respondendo às 10 perguntas estratégicas sobre os dados.")

    # --- Q1 ---
    with st.expander(
        "1. Qual Cidade com Maior Valor de Venda de 'Office Supplies'?", expanded=True
    ):
        df_q1 = df[df["Categoria"] == "Office Supplies"]
        if not df_q1.empty:
            city_max_sales = df_q1.groupby("Cidade")["Valor_Venda"].sum().idxmax()
            max_val = df_q1.groupby("Cidade")["Valor_Venda"].sum().max()
            st.metric("Cidade Vencedora", city_max_sales, f"R$ {max_val:,.2f}")
        else:
            st.warning("Dados insuficientes para esta categoria.")

    # --- Q2 ---
    with st.expander("2. Qual o Total de Vendas Por Data do Pedido?", expanded=True):
        if "Data_Pedido" in df.columns:
            df_q2 = df.groupby("Data_Pedido")["Valor_Venda"].sum().reset_index()
            fig_q2 = px.line(
                df_q2, x="Data_Pedido", y="Valor_Venda", title="Tendência de Vendas"
            )
            fig_q2.update_traces(line_color=COLOR_PALETTE[0])
            st.plotly_chart(fig_q2, use_container_width=True)

    # --- Q3 ---
    with st.expander("3. Qual o Total de Vendas por Estado?"):
        df_q3 = (
            df.groupby("Estado")["Valor_Venda"]
            .sum()
            .reset_index()
            .sort_values("Valor_Venda", ascending=False)
        )
        fig_q3 = px.bar(
            df_q3,
            x="Estado",
            y="Valor_Venda",
            color="Estado",
            title="Vendas por Estado",
        )
        fig_q3.update_layout(showlegend=False)
        st.plotly_chart(fig_q3, use_container_width=True)

    # --- Q4 ---
    with st.expander("4. Quais São as 10 Cidades com Maior Total de Vendas?"):
        df_q4 = (
            df.groupby("Cidade")["Valor_Venda"]
            .sum()
            .reset_index()
            .nlargest(10, "Valor_Venda")
        )
        fig_q4 = px.bar(
            df_q4, x="Cidade", y="Valor_Venda", color="Cidade", title="Top 10 Cidades"
        )
        fig_q4.update_layout(showlegend=False)
        st.plotly_chart(fig_q4, use_container_width=True)

    # --- Q5 ---
    with st.expander("5. Qual Segmento Teve o Maior Total de Vendas?"):
        df_q5 = (
            df.groupby("Segmento")["Valor_Venda"]
            .sum()
            .reset_index()
            .sort_values("Valor_Venda", ascending=False)
        )
        winner_segment = df_q5.iloc[0]["Segmento"]
        winner_value = df_q5.iloc[0]["Valor_Venda"]
        st.metric("Segmento Campeão", winner_segment, f"R$ {winner_value:,.2f}")
        plot_bar(
            df_q5,
            x_col="Valor_Venda",
            y_col="Segmento",
            orientation="h",
            color="Segmento",
            title="Total de Vendas por Segmento",
        )

    # --- Q6 ---
    with st.expander("6. Qual o Total de Vendas Por Segmento e Por Ano?"):
        if "Ano" in df.columns:
            df_q6 = df.groupby(["Ano", "Segmento"])["Valor_Venda"].sum().reset_index()
            fig_q6 = px.bar(
                df_q6,
                x="Ano",
                y="Valor_Venda",
                color="Segmento",
                barmode="group",
                title="Vendas por Ano e Segmento",
            )
            st.plotly_chart(fig_q6, use_container_width=True)

    # --- Q7 & Q8 ---
    with st.expander("7 & 8. Simulação de Descontos"):
        st.markdown(
            "**Regra:** Se Valor > 1000, Desconto de 15%. Caso contrário, 10% (apenas para classificação)."
        )
        st.markdown(
            "*Para o cálculo de média 'Depois', aplicou-se 15% apenas para vendas > 1000.*"
        )

        sales = df["Valor_Venda"]
        count_15 = (sales > 1000).sum()

        col_d1, col_d2, col_d3 = st.columns(3)
        col_d1.metric("Qtd. Vendas c/ 15% Off", count_15)

        avg_before = sales.mean()
        # Aplica 15% apenas onde > 1000, mantém o resto igual (conforme lógica legada para Q8)
        sales_after = np.where(sales > 1000, sales * 0.85, sales)
        avg_after = sales_after.mean()

        col_d2.metric("Média Antes", f"R$ {avg_before:,.2f}")
        col_d3.metric(
            "Média Depois",
            f"R$ {avg_after:,.2f}",
            delta=f"{avg_after - avg_before:,.2f}",
        )

    # --- Q9 ---
    with st.expander("9. Média de Vendas Por Segmento, Por Ano e Por Mês"):
        if "Ano_Mes" in df.columns:
            df_q9 = (
                df.groupby(["Segmento", "Ano_Mes"])["Valor_Venda"].mean().reset_index()
            )
            fig_q9 = px.line(
                df_q9,
                x="Ano_Mes",
                y="Valor_Venda",
                color="Segmento",
                title="Média Mensal por Segmento",
            )
            st.plotly_chart(fig_q9, use_container_width=True)

    # --- Q10 ---
    with st.expander("10. Total por Categoria e Top 12 SubCategorias"):
        st.markdown("Visualização hierárquica das vendas (Sunburst Chart).")
        # Top 12 Subcategorias
        top12_subs = df.groupby("SubCategoria")["Valor_Venda"].sum().nlargest(12).index
        df_top12 = df[df["SubCategoria"].isin(top12_subs)]

        fig_q10 = px.sunburst(
            df_top12,
            path=["Categoria", "SubCategoria"],
            values="Valor_Venda",
            color="Categoria",
            color_discrete_sequence=COLOR_PALETTE,
        )
        fig_q10.update_layout(height=600)
        st.plotly_chart(fig_q10, use_container_width=True)
