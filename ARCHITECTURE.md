# 🏗️ Arquitetura do Pipeline de Dados

Este documento detalha o desenho técnico e as decisões de engenharia adotadas no ecossistema de Auditoria de Custos e Conciliação Bancária.

## 🗂️ Visão Geral do Fluxo

O pipeline foi construído utilizando o conceito de **Medallion Architecture** (Arquitetura Medalhão), dividindo a responsabilidade de transformação em 3 camadas lógicas isoladas e acopladas de forma linear através do **DuckDB**.

[ Sistemas de Origem ]
│ (CSV)
▼
┌───────────────┐
│ Camada Bronze │ ──► Ingestão dos dados brutos (Raw)
└───────────────┘
│
▼
┌───────────────┐
│ Camada Silver │ ──► Limpeza, tipagem estrita e anonimização (LGPD)
└───────────────┘
│
▼
┌───────────────┐
│  Camada Gold  │ ──► Regras de negócio e Join de Conciliação
└───────────────┘
│
▼
[ Streamlit App ]  ──► Dashboard de Auditoria Executiva em tempo real

## 🥞 Stack Tecnológica

* **Python 3.11:** Linguagem base para desenvolvimento dos scripts de ETL.
* **DuckDB:** Engine de processamento analítico (OLAP) em memória, operando diretamente sobre arquivos Parquet e CSV com máxima eficiência computacional.
* **Pandas & PyArrow:** Suporte na manipulação de DataFrames e persistência em formato colunar de alta performance.
* **Streamlit:** Camada de apresentação visual (Frontend) para análise de métricas de negócio e CPFs com divergência.

## 🛡️ Decisões de Segurança e Performance
1. **Mascaramento de Dados (LGPD):** CPFs reais são tratados e transformados em hashes/máscaras parciais na transição da camada Bronze para a Silver.
2. **Eficiência de Memória (Caching):** O app frontend utiliza a diretiva `@st.cache_data` para evitar leituras redundantes de disco via DuckDB a cada mudança de filtro.
3. **Imunidade a Injeção:** Filtros do dashboard são resolvidos dinamicamente por meio de máscaras booleanas no Pandas, eliminando concatenações de strings no SQL.
