import os
import duckdb
import pandas as pd
import streamlit as st
from pathlib import Path

# 1. Configuração da página
st.set_page_config(
    page_title="Auditoria de Custos - Conciliação Bancária",
    page_icon="📊",
    layout="wide"
)

# 2. Resolução de Caminhos Robustos usando pathlib (Sugestão da imagem 1000147433.jpg)
BASE_DIR = Path(__file__).resolve().parent
GOLD_FILE = BASE_DIR / "../data/gold/conciliacao_final.parquet"

# 3. Função de Carga de Dados Otimizada com Caching e Tratamento de Erros
@st.cache_data(show_spinner="Carregando dados da Camada Gold...")
def load_gold_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        return pd.DataFrame() # Retorna dataframe vazio se não existir
    
    # Executa a query uma única vez e joga em memória de forma segura
    con = duckdb.connect()
    df = con.execute(f"SELECT * FROM read_parquet('{file_path}')").df()
    con.close()
    return df

# Verificação de Robustez: Arquivo existe?
if not GOLD_FILE.exists():
    st.error("❌ Arquivo da Camada Gold não encontrado!")
    st.markdown(f"O arquivo esperado em `{GOLD_FILE}` não foi localizado.")
    st.info("💡 **Como resolver:** Execute os scripts de ETL na ordem correta antes de abrir o painel:\n"
            "1. `python scripts/gerador_dados.py` (para criar os dados sintéticos)\n"
            "2. `python scripts/processamento_silver.py` (camada silver)\n"
            "3. `python scripts/conciliacao_gold.py` (camada gold)")
    st.stop()

# Carrega os dados utilizando o cache do Streamlit
df_total = load_gold_data(GOLD_FILE)

# 4. Cálculo das Métricas de Negócio (Baseado nos dados em memória)
total_tx = len(df_total)
df_divergentes = df_total[df_total["status_conciliacao"] == "Divergente"]
total_div = len(df_divergentes)
prejuizo = df_divergentes["diferenca_conciliacao"].sum() if total_div > 0 else 0.0

# 5. Interface Visual - Título e KPIs
st.title("📊 Painel de Auditoria de Custos & Conciliação")
st.markdown("### *Mapeamento e identificação de divergências financeiras (Operadora vs. Banco)*")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Volume Total Auditado", value=f"{total_tx:,} tx")
with col2:
    st.metric(
        label="Divergências Encontradas", 
        value=f"{total_div} ocorrências", 
        delta=f"-{total_div} críticas", 
        delta_color="inverse"
    )
with col3:
    st.metric(
        label="Vazamento de Receita (Rombo)", 
        value=f"R$ {abs(prejuizo):,.2f}", 
        delta="- Perda Financeira", 
        delta_color="normal"
    )

st.markdown("---")

# 6. Barra Lateral - Filtros de Auditoria
st.sidebar.header("🔍 Filtros de Auditoria")
status_selecionado = st.sidebar.selectbox(
    "Selecione o Status das Transações:",
    ["Todos", "Conciliado", "Divergente"]
)

# 7. Filtro Seguro usando Boolean Mask do Pandas (Elimina Risco de Injeção de SQL)
if status_selecionado == "Todos":
    df_filtrado = df_total.copy()
else:
    df_filtrado = df_total[df_total["status_conciliacao"] == status_selecionado]

# Renomeando as colunas para exibição profissional no frontend
df_exibicao = df_filtrado.rename(columns={
    "transaction_id": "ID Transação",
    "client_cpf": "CPF Cliente",
    "valor_liquido_operadora": "Líquido Operadora (R$)",
    "valor_liquido_banco": "Líquido Banco (R$)",
    "diferenca_conciliacao": "Diferença (R$)",
    "status_conciliacao": "Status"
})

# 8. Layout Gráfico e Tabela Otimizados
col_grafico, col_tabela = st.columns([1, 2])

with col_grafico:
    st.subheader("📈 Distribuição de Status")
    if not df_exibicao.empty:
        status_counts = df_exibicao["Status"].value_counts()
        st.bar_chart(status_counts, color="#1f77b4")
    else:
        st.warning("Sem dados para exibir o gráfico.")

with col_tabela:
    st.subheader("🔍 Registro Detalhado das Transações")
    st.markdown("Use os filtros laterais para isolar inconsistências e auditar CPFs.")
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("⚙️ Pipeline de Dados desenvolvido de forma segura com DuckDB & Caching Ativo.")
