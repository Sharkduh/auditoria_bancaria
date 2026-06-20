"""
Script de Conciliação - Camada Gold
Aplica regras de negócio e realiza join de conciliação entre operadora e banco.
"""

import pandas as pd
import random
from pathlib import Path

# Configurações
SILVER_FILE = Path("data/silver/silver_operadora.parquet")
GOLD_FILE = Path("data/gold/conciliacao_final.parquet")

# Criar diretório de saída
Path("data/gold").mkdir(parents=True, exist_ok=True)


def carregar_silver():
    """Carrega dados da camada Silver."""
    print("📂 Carregando dados da camada Silver...")
    df = pd.read_parquet(SILVER_FILE)
    print(f"  ✓ {len(df)} transações carregadas\n")
    return df


def simular_dados_banco(df):
    """
    Simula dados de repasse bancário.
    Em produção, isso viria de um arquivo de extratos do banco.
    """
    print("🏦 Simulando dados de repasse bancário...")

    # Criar lista de valores bancários
    valores_banco = []

    for idx, row in df.iterrows():
        valor_operadora = row["valor_liquido_operadora"]

        # 95% das vezes, o banco repassa o valor correto
        if random.random() < 0.95:
            valor_banco = valor_operadora
        else:
            # 5% das vezes há discrepância (erros, taxas indevidas, etc)
            valor_banco = valor_operadora * random.uniform(0.95, 0.99)

        valores_banco.append(valor_banco)

    df["valor_liquido_banco"] = valores_banco
    print(f"  ✓ Dados bancários simulados\n")

    return df


def calcular_diferenca_conciliacao(df):
    """
    Calcula a diferença de conciliação.
    Fórmula: diferenca = valor_operadora - valor_banco
    """
    print("🔢 Calculando diferenças de conciliação...")

    df["diferenca_conciliacao"] = df["valor_liquido_operadora"] - df["valor_liquido_banco"]

    # Arredondar para 2 casas decimais
    df["diferenca_conciliacao"] = df["diferenca_conciliacao"].round(2)

    print(f"  ✓ Diferenças calculadas\n")

    return df


def classificar_status_conciliacao(df):
    """
    Classifica o status de conciliação de cada transação.
    """
    print("📋 Classificando status de conciliação...")

    # Tolerância de R$ 0,01 para diferenças de arredondamento
    TOLERANCIA = 0.01

    def classificar(diferenca):
        if abs(diferenca) <= TOLERANCIA:
            return "Conciliado"
        else:
            return "Divergente"

    df["status_conciliacao"] = df["diferenca_conciliacao"].apply(classificar)

    # Calcular estatísticas
    conciliados = (df["status_conciliacao"] == "Conciliado").sum()
    divergentes = (df["status_conciliacao"] == "Divergente").sum()
    taxa_sucesso = (conciliados / len(df)) * 100

    print(f"  ✓ Transações Conciliadas: {conciliados} ({taxa_sucesso:.2f}%)")
    print(f"  ✓ Transações Divergentes: {divergentes} ({100-taxa_sucesso:.2f}%)\n")

    return df


def calcular_kpis(df):
    """
    Calcula KPIs para análise de negócio.
    """
    print("📊 Calculando KPIs...")

    total_vazamento = df[df["status_conciliacao"] == "Divergente"][
        "diferenca_conciliacao"
    ].abs().sum()

    print(f"  ✓ Vazamento total de receita: R$ {total_vazamento:,.2f}")
    print(f"  ✓ Vazamento médio por transação: R$ {total_vazamento / len(df):,.2f}")
    print(f"  ✓ Volume total auditado: R$ {df['valor_liquido_operadora'].sum():,.2f}\n")

    return total_vazamento


def procesar_gold():
    """
    Pipeline completo da camada Gold.
    """
    print("🥇 Iniciando processamento da Camada Gold...\n")

    # 1. Carregar dados da Silver
    df = carregar_silver()

    # 2. Simular dados do banco
    df = simular_dados_banco(df)

    # 3. Calcular diferenças
    df = calcular_diferenca_conciliacao(df)

    # 4. Classificar status
    df = classificar_status_conciliacao(df)

    # 5. Calcular KPIs
    total_vazamento = calcular_kpis(df)

    # 6. Selecionar colunas finais
    df_final = df[
        [
            "id_transacao",
            "cpf_cliente",
            "valor_liquido_operadora",
            "valor_liquido_banco",
            "diferenca_conciliacao",
            "status_conciliacao",
            "data_transacao",
        ]
    ]

    # 7. Salvar em Parquet
    print(f"💾 Salvando em {GOLD_FILE}...")
    df_final.to_parquet(GOLD_FILE, index=False, compression="snappy")
    print(f"  ✓ Arquivo salvo com sucesso!\n")

    print("✨ Processamento da Camada Gold concluído!")
    print(f"   📊 Total de transações processadas: {len(df_final)}")
    print(f"   💰 Vazamento total detectado: R$ {total_vazamento:,.2f}")

    return df_final


if __name__ == "__main__":
    df_gold = procesar_gold()
