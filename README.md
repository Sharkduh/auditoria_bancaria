# 📊 Pipeline de Conciliação Bancária & Auditoria de Custos

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Fast_SQL-orange.svg)](https://duckdb.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io/)

Um pipeline de engenharia de dados de ponta a ponta focado em governança financeira e contenção de vazamento de receita. O projeto simula o cenário real de uma empresa que precisa auditar e conciliar os repasses de uma operadora de cartões contra os créditos efetivados na conta bancária.

---

## 🎯 Cenário de Negócio & Problema

Inconsistências em repasses financeiros e taxas cobradas incorretamente por adquirentes/bancos geram um impacto silencioso no caixa das empresas (vazamento de receita). 

**O Objetivo:** Automatizar a auditoria de transações em larga escala, identificando centavo por centavo se o valor líquido calculado pela operadora bate perfeitamente com o saldo recebido no banco, isolando fraudes, falhas operacionais ou quebras de contrato.

---

## 🏗️ Arquitetura de Dados (Medallion Architecture)

O projeto foi estruturado seguindo as melhores práticas de governança de dados do mercado:

1. **Camada Bronze (Raw):** Ingestão e armazenamento dos arquivos brutos em formato CSV (`relatorio_operadora.csv` e `vendas_banco.csv`) direto da fonte.
2. **Camada Silver (Trusted):** Limpeza, tipagem analítica de dados e tratamento de sensibilidade/LGPD (normalização e limpeza de strings de CPF usando Expressões Regulares/Regex). Armazenamento otimizado no formato colunar **Parquet**.
3. **Camada Gold (Business):** Aplicação das regras de negócio. Cruzamento de dados via SQL (`INNER JOIN` por ID de transação) e cálculo analítico de divergências, gerando a base final de conciliação.

---

## ⚡ Decisões de Infraestrutura & Engenharia Eficiente

* **DuckDB sobre PySpark:** Como o projeto foi desenhado para rodar localmente com alta performance e restrição de recursos de hardware (ambiente leve), optou-se pelo uso do **DuckDB**. Ele processa dados em memória utilizando o poder do SQL analítico vetorizado, entregando velocidade comparável a clusters de Big Data sem o overhead de memória do JVM/Spark.
* **Apache Arrow & Parquet:** Substituição de arquivos de texto tradicionais por arquivos Parquet. O formato colunar garantiu alta compactação, leitura ultra-rápida e integração nativa e eficiente com a camada de visualização.

---

## 📊 Resultados do Processamento & Impacto Financeiro

Ao rodar o pipeline de auditoria, o sistema processou e cruzou com sucesso o volume de dados gerando os seguintes insights:

* **Total de Transações Auditadas:** 4.988
* **Transações Conciliadas (Sucesso):** 4.933 (Conformidade total)
* **Transações Divergentes (Alerta Crítico):** 55 ocorrências
* **Vazamento de Receita Identificado (Rombo):** **-R$ 207,63** de perda financeira para ação do time de contas a receber.

---

## 🖥️ Camada de Visualização (Streamlit Dashboard)

Para dar suporte à tomada de decisão executiva, foi desenvolvido um painel interativo utilizando **Streamlit**, permitindo que analistas financeiros e auditores filtrem transações por status, monitorem os KPIs de risco em tempo real e inspecionem os CPFs associados às quebras de repasse.

---

## 🛠️ Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/projeto_conciliacao_bancaria.git](https://github.com/SEU_USUARIO/projeto_conciliacao_bancaria.git)
   cd projeto_conciliacao_bancaria

2  **Crie e ative seu ambiente virtual:**

  python -m venv .venv
   source .venv/bin/activate

3 **Instale as dependências contidas no manifesto:**

pip install -r requirements.txt

4 **Execute o ecossistema de scripts na ordem cronológica do Pipeline:**

# Passo A: Gerar a base de dados bruta (Camada Bronze)
   python scripts/gerador_dados.py

   # Passo B: Executar a limpeza e mascaramento de sensibilidade (Camada Silver)
   python scripts/processamento_silver.py

   # Passo C: Aplicar regras de negócio e join de conciliação (Camada Gold)
   python scripts/conciliacao_gold.py

5 **streamlit run scripts/app_dashboard.py**

streamlit run scripts/app_dashboard.py
