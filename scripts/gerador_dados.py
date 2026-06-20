"""
Script de Geração de Dados - Camada Bronze
Gera dados simulados de transações de vendas pela operadora de cartões.
"""

import os
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configurações
NUM_TRANSACTIONS = 10000
DATA_DIR = Path("data/bronze")
OUTPUT_FILE = DATA_DIR / "vendas_operadora.csv"

# Criar diretório se não existir
DATA_DIR.mkdir(parents=True, exist_ok=True)


def gerar_cpf_simulado():
    """Gera um CPF simulado para teste."""
    return f"{random.randint(10000000000, 99999999999)}"


def gerar_dados_transacoes():
    """Gera dados simulados de transações."""
    transacoes = []
    base_date = datetime.now() - timedelta(days=30)

    for i in range(NUM_TRANSACTIONS):
        transaction_id = f"TRX{i+1:08d}"
        cpf_cliente = gerar_cpf_simulado()
        valor_bruto = round(random.uniform(10.0, 5000.0), 2)
        taxa_cobrada = round(random.choice([0.02, 0.025, 0.03, 0.035]), 4)  # 2-3.5%

        # Adicionar algumas discrepâncias intencionais para teste
        if random.random() < 0.05:  # 5% de chance de divergência
            taxa_cobrada = round(taxa_cobrada * random.uniform(1.1, 1.5), 4)

        transacoes.append({
            "id_transacao": transaction_id,
            "cpf_cliente": cpf_cliente,
            "valor_bruto": valor_bruto,
            "taxa_cobrada": taxa_cobrada,
            "data_transacao": base_date + timedelta(days=random.randint(0, 29)),
        })

    return transacoes


def salvar_dados_csv(transacoes):
    """Salva dados em arquivo CSV."""
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "id_transacao",
            "cpf_cliente",
            "valor_bruto",
            "taxa_cobrada",
            "data_transacao",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for transacao in transacoes:
            writer.writerow(transacao)

    print(f"✅ Arquivo gerado com sucesso: {OUTPUT_FILE}")
    print(f"📊 Total de transações: {len(transacoes)}")


if __name__ == "__main__":
    print("🔄 Gerando dados da Camada Bronze...")
    transacoes = gerar_dados_transacoes()
    salvar_dados_csv(transacoes)
    print("✨ Dados gerados com sucesso!")
