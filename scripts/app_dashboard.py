import os
import duckdb
import streamlit as st

# 1. Configuração da página do Streamlit (Layout corporativo amplo)
st.set_page_config(
    page_title="Auditoria de Custos - Conciliação Bancária",
    page_icon="📊",
    layout="wide"
)

# Estilização CSS customizada para deixar os KPIs ainda mais chamativos
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Auditoria de Custos & Conciliação")
st.markdown("### *Mapeamento e identificação de divergências financeiras (Operadora vs. Banco)*")
st.markdown("---")

# 2. Caminho do arquivo Gold
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GOLD_FILE = os.path.join(BASE_DIR, "../data/gold/conciliacao_final.parquet")

con = duckdb.connect()

# Puxar métricas agregadas para os cartões (KPIs)
metrics = con.execute(f"""
    SELECT 
        COUNT(*) AS total_transacoes,
        COUNT(CASE WHEN status_conciliacao = 'Divergente' THEN 1 END) AS total_divergentes,
        COALESCE(SUM(CASE WHEN status_conciliacao = 'Divergente' THEN diferenca_conciliacao END), 0) AS valor_rombo
    FROM read_parquet('{GOLD_FILE}')
""").fetchone()

total_tx, total_div, prejuizo = metrics

# 3. Exibição dos KPIs em Linha (Estilo Executivo)
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/584/584013.png", width=40)
    st.metric(label="Volume Total Auditado", value=f"{total_tx:,} tx")

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/564/564619.png", width=40)
    st.metric(
        label="Divergências Encontradas", 
        value=f"{total_div} ocorrências", 
        delta=f"-{total_div} críticas", 
        delta_color="inverse"
    )

with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/2454/2454261.png", width=40)
    # Exibindo o prejuízo como positivo no card, mas com o delta explicitando o impacto negativo
    st.metric(
        label="Vazamento de Receita (Rombo)", 
        value=f"R$ {abs(prejuizo):,.2f}", 
        delta="- Perda Financeira", 
        delta_color="normal"
    )

st.markdown("---")

# 4. Filtro interativo na barra lateral
st.sidebar.header("🔍 Filtros de Auditoria")
status_selecionado = st.sidebar.selectbox(
    "Selecione o Status das Transações:",
    ["Todos", "Conciliado", "Divergente"]
)

if status_selecionado == "Todos":
    where_clause = ""
else:
    where_clause = f"WHERE status_conciliacao = '{status_selecionado}'"

# 5. Correção do Erro de Sintaxe: Uso de aspas duplas em vez de colchetes
df_detalhado = con.execute(f"""
    SELECT 
        transaction_id AS "ID Transação",
        client_cpf AS "CPF Cliente",
        valor_liquido_operadora AS "Líquido Operadora (R$)",
        valor_liquido_banco AS "Líquido Banco (R$)",
        diferenca_conciliacao AS "Diferença (R$)",
        status_conciliacao AS "Status"
    FROM read_parquet('{GOLD_FILE}')
    {where_clause}
""").df()

# 6. Layout em duas colunas para Gráfico e Dados (Otimiza o espaço na tela)
col_grafico, col_tabela = st.columns([1, 2])

with col_grafico:
    st.subheader("📈 Distribuição de Status")
    # Gráfico de barras simples com contagem absoluta dos dados filtrados
    status_counts = df_detalhado["Status"].value_counts()
    st.bar_chart(status_counts, color="#1f77b4")

with col_tabela:
    st.subheader("🔍 Registro Detalhado das Transações")
    st.markdown("Use os filtros laterais para isolar inconsistências e auditar CPFs.")
    # Exibe o dataframe com largura total e formatação limpa
    st.dataframe(df_detalhado, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("⚙️ Pipeline de Dados desenvolvido com a Arquitetura Medalhão utilizando DuckDB & Parquet.")
