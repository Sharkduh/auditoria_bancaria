import os
import duckdb

print("✨ Iniciando o Processamento da Camada Gold (Conciliação Final)...")

# 1. Definir caminhos das pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SILVER_DIR = os.path.join(BASE_DIR, "../data/silver")
GOLD_DIR = os.path.join(BASE_DIR, "../data/gold")

# Garantir que a pasta Gold existe no Pendrive
os.makedirs(GOLD_DIR, exist_ok=True)

# 2. Inicializar a conexão com o DuckDB
con = duckdb.connect()

print("⏳ Cruzando dados da Operadora com o Banco via SQL...")
# Query de conciliação aplicando a lógica de negócio
query_gold = f"""
    SELECT 
        o.transaction_id,
        b.client_cpf,
        o.gross_amount AS valor_bruto_operadora,
        o.fee_amount AS taxa_operadora,
        o.net_amount AS valor_liquido_operadora,
        b.bank_fee AS taxa_bancaria,
        b.net_amount AS valor_liquido_banco,
        (o.net_amount - b.net_amount) AS diferenca_conciliacao,
        CASE 
            WHEN (o.net_amount - b.net_amount) = 0 THEN 'Conciliado'
            ELSE 'Divergente'
        END AS status_conciliacao
    FROM read_parquet('{SILVER_DIR}/operadora_limpa.parquet') o
    INNER JOIN read_parquet('{SILVER_DIR}/banco_limpo.parquet') b
    ON o.transaction_id = b.transaction_id
"""

# Executa e salva o relatório final na Gold em formato Parquet
con.execute(f"""
    COPY ({query_gold}) 
    TO '{GOLD_DIR}/conciliacao_final.parquet' 
    (FORMAT PARQUET)
""")
print("✅ Relatório de conciliação gerado e salvo na Gold!")

# 3. Mostrar um resumo do resultado na tela para auditoria
print("\n📊 --- RESUMO DA AUDITORIA DE CUSTOS ---")
df_resumo = con.execute(f"""
    SELECT 
        status_conciliacao, 
        COUNT(*) AS quantidade_transacoes,
        SUM(diferenca_conciliacao) AS total_divergencia
    FROM read_parquet('{GOLD_DIR}/conciliacao_final.parquet')
    GROUP BY status_conciliacao
""").df()

print(df_resumo)
print("\n🏁 Projeto de Conciliação concluído com sucesso absoluto!")
