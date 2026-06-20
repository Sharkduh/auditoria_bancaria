"""
Script de Processamento - Camada Silver
Realiza limpeza, tipagem estrita e mascaramento de dados sensíveis (LGPD).
"""

import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
import hashlib

# Configurações
BRONZE_FILE = Path("data/bronze/vendas_operadora.csv")
SILVER_FILE = Path("data/silver/silver_operadora.parquet")

# Criar diretório de saída
Path("data/silver").mkdir(parents=True, exist_ok=True)


def mascarar_cpf(cpf_str):
    """
    Mascara CPF de acordo com conformidade LGPD.
    Formato: ***123***00 (apenas últimos 2 dígitos visíveis)
    """
    if not cpf_str or len(str(cpf_str)) < 4:
        return "***.***.***-**"

    cpf_str = str(cpf_str).strip()
    if len(cpf_str) >= 11:
        # Formato: primeiros 3 + meio oculto + últimos 2
        return f"***{cpf_str[3:6]}***{cpf_str[-2:]}"
    else:
        return "***.***.***-**"


def limpar_dados(df):
    """
    Realiza limpeza e validação dos dados.
    """
    print("🧹 Limpando dados...")

    # Remover duplicatas
    initial_rows = len(df)
    df = df.drop_duplicates(subset=["id_transacao"], keep="first")
    print(f"  - Duplicatas removidas: {initial_rows - len(df)}")

    # Tratamento de nulos
    df = df.dropna()
    print(f"  - Linhas com nulos removidas: {initial_rows - len(df)}")

    return df


def aplicar_tipagem(df):
    """
    Aplica tipagem estrita aos dados.
    """
    print("📝 Aplicando tipagem...")

    df["id_transacao"] = df["id_transacao"].astype(str)
    df["cpf_cliente"] = df["cpf_cliente"].astype(str)
    df["valor_bruto"] = pd.to_numeric(df["valor_bruto"], errors="coerce")
    df["taxa_cobrada"] = pd.to_numeric(df["taxa_cobrada"], errors="coerce")
    df["data_transacao"] = pd.to_datetime(df["data_transacao"], errors="coerce")

    # Remover linhas onde conversão falhou
    df = df.dropna()

    return df


def calcular_valor_liquido(df):
    """
    Calcula o valor líquido após aplicação de taxa.
    Fórmula: valor_liquido = valor_bruto * (1 - taxa)
    """
    print("💰 Calculando valor líquido...")

    df["valor_liquido_operadora"] = df["valor_bruto"] * (1 - df["taxa_cobrada"])

    return df


def mascarar_dados_sensiveis(df):
    """
    Aplica mascaramento de dados sensíveis (LGPD).
    """
    print("🔒 Mascarando dados sensíveis (LGPD)...")

    df["cpf_cliente"] = df["cpf_cliente"].apply(mascarar_cpf)

    return df


def processar_silver():
    """
    Pipeline completo da camada Silver.
    """
    print("🥈 Iniciando processamento da Camada Silver...\n")

    # 1. Carregar dados
    print(f"📂 Carregando dados de {BRONZE_FILE}...")
    df = pd.read_csv(BRONZE_FILE)
    print(f"  ✓ {len(df)} linhas carregadas\n")

    # 2. Limpar dados
    df = limpar_dados(df)
    print(f"  ✓ Limpeza concluída: {len(df)} linhas\n")

    # 3. Aplicar tipagem
    df = aplicar_tipagem(df)
    print(f"  ✓ Tipagem aplicada: {len(df)} linhas\n")

    # 4. Calcular valor líquido
    df = calcular_valor_liquido(df)
    print(f"  ✓ Valor líquido calculado\n")

    # 5. Mascarar dados sensíveis
    df = mascarar_dados_sensiveis(df)
    print(f"  ✓ Dados mascarados conforme LGPD\n")

    # 6. Selecionar colunas finais
    df_final = df[
        [
            "id_transacao",
            "cpf_cliente",
            "valor_bruto",
            "taxa_cobrada",
            "valor_liquido_operadora",
            "data_transacao",
        ]
    ]

    # 7. Salvar em Parquet
    print(f"💾 Salvando em {SILVER_FILE}...")
    df_final.to_parquet(SILVER_FILE, index=False, compression="snappy")
    print(f"  ✓ Arquivo salvo com sucesso!\n")

    print("✨ Processamento da Camada Silver concluído!")
    print(f"   📊 Total de registros processados: {len(df_final)}")

    return df_final


if __name__ == "__main__":
    df_silver = processar_silver()
