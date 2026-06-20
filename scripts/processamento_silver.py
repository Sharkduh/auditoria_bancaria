import os
import duckdb

print("🚀 Iniciando o Processamento da Camada Silver...")

# 1. Definir caminhos das pastas usando caminhos relativos ao script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRONZE_DIR = os.path.join(BASE_DIR, "../data/bronze")
SILVER_DIR = os.path.join(BASE_DIR, "../data/silver")

# Garantir que a pasta Silver existe no Pendrive
os.makedirs(SILVER_DIR, exist_ok=True)

# 2. Inicializar a conexão com o DuckDB
con = duckdb.connect()

print("⏳ Tratando dados da Operadora...")
# Ajustado para usar 'operator_fee' que está no seu CSV
query_operadora = f"""
    SELECT 
        transaction_id,
        processing_date,
        gross_amount,
        operator_fee AS fee_amount,
        net_amount
    FROM read_csv_auto('{BRONZE_DIR}/relatorio_operadora.csv')
    WHERE transaction_id IS NOT NULL
"""

# Executa a query e salva em PARQUET
con.execute(f"""
    COPY ({query_operadora}) 
    TO '{SILVER_DIR}/operadora_limpa.parquet' 
    (FORMAT PARQUET)
""")
print("✅ Operadora processada e salva em Parquet!")


print("⏳ Tratando dados do Banco (Limpando CPF)...")
query_banco = f"""
    SELECT 
        transaction_id,
        REGEXP_REPLACE(CAST(client_cpf AS VARCHAR), '[.-]', '', 'g') AS client_cpf,
        bank_fee,
        net_amount
    FROM read_csv_auto('{BRONZE_DIR}/vendas_banco.csv')
    WHERE transaction_id IS NOT NULL
"""

# Executa e salva em Parquet
con.execute(f"""
    COPY ({query_banco}) 
    TO '{SILVER_DIR}/banco_limpo.parquet' 
    (FORMAT PARQUET)
""")
print("✅ Banco processado e salvo em Parquet!")

print("🏁 Camada Silver concluída com sucesso absoluto!")
