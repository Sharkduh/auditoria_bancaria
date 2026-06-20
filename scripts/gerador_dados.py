import csv
import random
from datetime import datetime, timedelta

# Configurações iniciais
NUM_TRANSACOES = 5000
DATA_INICIO = datetime(2026, 6, 1)

vendas_banco = []
relatorio_operadora = []

print("Gerando dados sintéticos de conciliação...")

for i in range(1, NUM_TRANSACOES + 1):
    tx_id = f"TX_202606_{i:05d}"
    cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
    valor_bruto = round(random.uniform(10.0, 1500.0), 2)
    
    # Regra de negócio contratada pelo banco: Taxa de 2.0%
    taxa_contratada = 0.02
    tarifa_banco = round(valor_bruto * taxa_contratada, 2)
    valor_liquido_banco = round(valor_bruto - tarifa_banco, 2)
    
    data_transacao = DATA_INICIO + timedelta(seconds=random.randint(0, 86400 * 5))
    data_str = data_transacao.strftime("%Y-%m-%d %H:%M:%S")
    
    # Adiciona na visão do Banco
    vendas_banco.append([tx_id, cpf, data_str, valor_bruto, tarifa_banco, valor_liquido_banco])
    
    # Simulação de erros para o pipeline pegar
    erro_random = random.random()
    
    if erro_random < 0.01:
        # Erro Tipo 1: Operadora cobrou taxa errada (2.5% em vez de 2%)
        taxa_errada = 0.025
        tarifa_op = round(valor_bruto * taxa_errada, 2)
        valor_liq_op = round(valor_bruto - tarifa_op, 2)
        relatorio_operadora.append([tx_id, data_str, valor_bruto, tarifa_op, valor_liq_op])
        
    elif erro_random < 0.02:
        # Erro Tipo 2: Transação sumiu do relatório da operadora (Vazamento de Receita)
        continue
        
    elif erro_random < 0.025:
        # Erro Tipo 3: Duplicidade no relatório da operadora
        tarifa_op = tarifa_banco
        valor_liq_op = valor_liquido_banco
        relatorio_operadora.append([tx_id, data_str, valor_bruto, tarifa_op, valor_liq_op])
        relatorio_operadora.append([tx_id, data_str, valor_bruto, tarifa_op, valor_liq_op])
        
    else:
        # Cenário Normal: Match perfeito
        tarifa_op = tarifa_banco
        valor_liq_op = valor_liquido_banco
        relatorio_operadora.append([tx_id, data_str, valor_bruto, tarifa_op, valor_liq_op])

# Salvando os arquivos na camada BRONZE no Pendrive
with open('../data/bronze/vendas_banco.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['transaction_id', 'client_cpf', 'transaction_date', 'gross_amount', 'bank_fee', 'net_amount'])
    writer.writerows(vendas_banco)

with open('../data/bronze/relatorio_operadora.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['transaction_id', 'processing_date', 'gross_amount', 'operator_fee', 'net_amount'])
    writer.writerows(relatorio_operadora)

print("Sucesso! Arquivos salvos em data/bronze/")
