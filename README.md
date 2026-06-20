# 📊 Pipeline de Conciliação Bancária & Auditoria de Custos

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![DuckDB](https://img.shields.io/badge/DuckDB-Latest-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Yes-red?style=for-the-badge&logo=streamlit)
![CI/CD](https://img.shields.io/badge/Pipeline-Verified-green?style=for-the-badge)

Um pipeline de engenharia de dados de ponta a ponta focado em governança financeira e contenção de vazamento de receita. O projeto simula o cenário real de uma empresa que precisa auditar e conciliar os repasses de uma operadora de cartões contra os créditos efetivados na conta bancária.

---

## 🎯 Cenário de Negócio & Problema

Inconsistências em repasses financeiros e taxas cobradas incorretamente por adquirentes/bancos geram um impacto silencioso no caixa das empresas (vazamento de receita).

**O Objetivo:** Automatizar a auditoria de transações em larga escala, identificando centavo por centavo se o valor líquido calculado pela operadora bate perfeitamente com o saldo recebido no banco, isolando fraudes, falhas operacionais ou quebras de contrato.

---

## 🏗️ Arquitetura de Dados (Medallion Architecture)

O projeto foi estruturado seguindo as melhores práticas de governança de dados do mercado:

1. **Camada Bronze (Raw):** Ingestão e armazenamento dos arquivos brutos em formato CSV.
2. **Camada Silver (Cleaned):** Limpeza de dados, tipagem estrita, tratamento de nulos e mascaramento de dados sensíveis (LGPD) salvos em formato colunar Parquet.
3. **Camada Gold (Analytical):** Processamento das regras de negócio, join de reconciliação e cruzamento analítico gerando o dataset final.

---

### 1. Clonar o Repositório
```bash
git clone https://github.com/Sharkduh/auditoria_bancaria.git
cd auditoria_bancaria

2. Crie e ative seu ambiente virtual:
python -m venv .venv
source .venv/bin/activate

3. Instale as dependências contidas no manifesto:
Bash
pip install -r requirements.txt

4. Execute o ecossistema de scripts na ordem cronológica do Pipeline:

Passo A: Gerar a base de dados bruta (Camada Bronze)
python scripts/gerador_dados.py

Passo B: Executar a limpeza e mascaramento de sensibilidade (Camada Silver)
python scripts/processamento_silver.py

Passo C: Aplicar regras de negócio e join de conciliação (Camada Gold)
python scripts/conciliacao_gold.py

5. Executar o Painel de Auditoria Executiva
streamlit run scripts/app_dashboard.py


🛡️ Governança e Qualidade

CI/CD: Pipeline integrado via GitHub Actions para validação automatizada de código.
Segurança: Secrets e variáveis estruturadas sob padrão
Licença: Distribuído sob os termos da licença MIT.
```bash
