# 📖 Dicionário de Dados do Repositório

Este documento descreve a estrutura dos schemas das tabelas em cada estágio de maturação do Pipeline.

## 🥉 Camada Bronze (Arquivos Iniciais)

### Dataset: `vendas_operadora.csv`
Representa os registros gerados pela adquirente de cartões.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id_transacao` | TEXT | Identificador único da transação gerado na maquininha/gateway. |
| `cpf_cliente` | TEXT | CPF sem formatação do comprador. |
| `valor_bruto` | TEXT | Valor total passado pelo cliente antes das taxas. |
| `taxa_cobrada` | TEXT | Percentual de taxa acordado em contrato. |

---

## 🥈 Camada Silver (Tratados e Higienizados)

### Dataset: `silver_operadora.parquet`
Dados limpos e estruturados com tipagem estrita e mascaramento ativo.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `transaction_id` | VARCHAR | Chave primária da transação. |
| `client_cpf` | VARCHAR | CPF mascarado ex: `***.123.***-00` para conformidade com a LGPD. |
| `valor_liquido_operadora` | DOUBLE | Valor líquido calculado de forma matemática: `valor_bruto * (1 - taxa)`. |

---

## 🥇 Camada Gold (Visão Analítica e Final)

### Dataset: `conciliacao_final.parquet`
Resultado do join de conciliação unificando a visão da Operadora vs. Banco.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `transaction_id` | VARCHAR | Chave única de amarração. |
| `client_cpf` | VARCHAR | Identificação protegida do cliente. |
| `valor_liquido_operadora` | DOUBLE | Valor que a operadora alegou que iria depositar. |
| `valor_liquido_banco` | DOUBLE | Valor que o banco efetivamente creditou na conta empresarial. |
| `diferenca_conciliacao` | DOUBLE | Subtração matemática: `valor_liquido_operadora - valor_liquido_banco`. |
| `status_conciliacao` | VARCHAR | Classificação da transação: `Conciliado` (diferença zero) ou `Divergente`. |
