"""
Dashboard Streamlit - Auditoria de Conciliação Bancária
Interface interativa para análise de divergências e KPIs de negócio.
"""

import streamlit as st
import pandas as pd
import duckdb
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Auditoria Bancária",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Arquivo de dados
GOLD_FILE = Path("data/gold/conciliacao_final.parquet")


@st.cache_data
def carregar_dados():
    """Carrega dados da camada Gold com cache."""
    if not GOLD_FILE.exists():
        st.error("❌ Arquivo de dados não encontrado!")
        st.info("Execute os scripts: gerador_dados.py → processamento_silver.py → conciliacao_gold.py")
        st.stop()

    df = pd.read_parquet(GOLD_FILE)
    return df


def main():
    # Header
    st.markdown("# 📊 Dashboard de Auditoria Bancária")
    st.markdown(
        "Análise em tempo real de conciliação entre operadora de cartões e banco"
    )

    # Carregar dados
    df = carregar_dados()

    # Sidebar - Filtros
    st.sidebar.markdown("## 🔍 Filtros")

    # Filtro por Status
    status_options = ["Todos"] + list(df["status_conciliacao"].unique())
    status_filtro = st.sidebar.selectbox("Status de Conciliação:", status_options)

    # Filtro por Período
    df["data_transacao"] = pd.to_datetime(df["data_transacao"])
    data_min = df["data_transacao"].min()
    data_max = df["data_transacao"].max()

    date_range = st.sidebar.date_input(
        "Período:",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
    )

    # Aplicar filtros
    df_filtrado = df.copy()

    if status_filtro != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["status_conciliacao"] == status_filtro
        ]

    if len(date_range) == 2:
        df_filtrado = df_filtrado[
            (df_filtrado["data_transacao"].dt.date >= date_range[0])
            & (df_filtrado["data_transacao"].dt.date <= date_range[1])
        ]

    # ==================== KPIs ====================
    st.markdown("## 📈 KPIs Principais")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_transacoes = len(df_filtrado)
        st.metric("Total de Transações", f"{total_transacoes:,}")

    with col2:
        conciliadas = (df_filtrado["status_conciliacao"] == "Conciliado").sum()
        st.metric("Conciliadas", f"{conciliadas:,}")

    with col3:
        divergentes = (df_filtrado["status_conciliacao"] == "Divergente").sum()
        st.metric("Divergentes", f"{divergentes:,}")

    with col4:
        taxa_sucesso = (conciliadas / total_transacoes * 100) if total_transacoes > 0 else 0
        st.metric("Taxa de Sucesso", f"{taxa_sucesso:.2f}%")

    # ==================== Vazamento de Receita ====================
    st.markdown("## 💰 Análise de Vazamento")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_operadora = df_filtrado["valor_liquido_operadora"].sum()
        st.metric("Volume Operadora", f"R$ {total_operadora:,.2f}")

    with col2:
        total_banco = df_filtrado["valor_liquido_banco"].sum()
        st.metric("Volume Banco", f"R$ {total_banco:,.2f}")

    with col3:
        vazamento_total = (df_filtrado["diferenca_conciliacao"].abs()).sum()
        st.metric("Vazamento Total", f"R$ {vazamento_total:,.2f}", delta=f"-R$ {vazamento_total:,.2f}")

    # ==================== Gráficos ====================
    st.markdown("## 📊 Visualizações")

    col1, col2 = st.columns(2)

    # Gráfico 1: Status de Conciliação (Pizza)
    with col1:
        status_counts = df_filtrado["status_conciliacao"].value_counts()
        fig_pizza = go.Figure(
            data=[
                go.Pie(
                    labels=status_counts.index,
                    values=status_counts.values,
                    hole=0.3,
                    marker=dict(
                        colors=["#28a745", "#dc3545"]
                    ),
                )
            ]
        )
        fig_pizza.update_layout(
            title="Distribuição de Status",
            height=400,
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

    # Gráfico 2: Diferenças de Conciliação (Histograma)
    with col2:
        divergentes_df = df_filtrado[
            df_filtrado["status_conciliacao"] == "Divergente"
        ]
        if len(divergentes_df) > 0:
            fig_hist = go.Figure(
                data=[
                    go.Histogram(
                        x=divergentes_df["diferenca_conciliacao"],
                        nbinsx=30,
                        marker=dict(color="#ff7300"),
                    )
                ]
            )
            fig_hist.update_layout(
                title="Distribuição de Divergências",
                xaxis_title="Diferença (R$)",
                yaxis_title="Frequência",
                height=400,
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Nenhuma divergência encontrada no período selecionado.")

    # ==================== Tabela de Divergências ====================
    st.markdown("## 📋 Transações Divergentes")

    divergentes = df_filtrado[
        df_filtrado["status_conciliacao"] == "Divergente"
    ].sort_values("diferenca_conciliacao", ascending=False)

    if len(divergentes) > 0:
        # Formatar colunas para exibição
        divergentes_display = divergentes.copy()
        divergentes_display["valor_liquido_operadora"] = divergentes_display[
            "valor_liquido_operadora"
        ].apply(lambda x: f"R$ {x:,.2f}")
        divergentes_display["valor_liquido_banco"] = divergentes_display[
            "valor_liquido_banco"
        ].apply(lambda x: f"R$ {x:,.2f}")
        divergentes_display["diferenca_conciliacao"] = divergentes_display[
            "diferenca_conciliacao"
        ].apply(lambda x: f"R$ {x:,.2f}")

        st.dataframe(
            divergentes_display[
                [
                    "id_transacao",
                    "cpf_cliente",
                    "valor_liquido_operadora",
                    "valor_liquido_banco",
                    "diferenca_conciliacao",
                ]
            ],
            use_container_width=True,
        )
    else:
        st.success("✅ Nenhuma transação divergente encontrada!")

    # ==================== Rodapé ====================
    st.markdown("---")
    st.markdown(
        """
        **📊 Pipeline de Auditoria Bancária**  
        Desenvolvido com Python, DuckDB, Pandas e Streamlit  
        [GitHub](https://github.com/Sharkduh/auditoria_bancaria) | 
        [LinkedIn](https://www.linkedin.com/in/eduardodossantosmiranda)
        """
    )


if __name__ == "__main__":
    main()
