# 📊 Pipeline de Conciliação Bancária & Auditoria de Custos

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![DuckDB](https://img.shields.io/badge/DuckDB-1.0.0-orange?style=for-the-badge&logo=duckdb)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Automated-brightgreen?style=for-the-badge)

Um pipeline de engenharia de dados de **ponta a ponta** focado em governança financeira e contenção de vazamento de receita. O projeto simula o cenário real de uma empresa que precisa auditar e conciliar transações de forma automatizada, identificando discrepâncias entre o que foi repassado pela operadora e o que foi efetivamente creditado no banco.

---

## 🎯 Cenário de Negócio & Problema

Inconsistências em repasses financeiros e taxas cobradas incorretamente por adquirentes/bancos geram um **impacto silencioso no caixa das empresas** (vazamento de receita).

**O Objetivo:** Automatizar a auditoria de transações em larga escala, identificando **centavo por centavo** se o valor líquido calculado pela operadora bate perfeitamente com o saldo recebido no banco, com máxima eficiência e zero fraude manual.

### 💰 Impacto Quantificável

| Métrica | Antes (Manual) | Depois (Automatizado) |
|---------|---|---|
| ⏱️ Tempo de Processamento | Horas/Dias em Excel | < 2 Segundos |
| 📊 Volume de Transações | ~1M linhas (Excel trava) | Dezenas de milhões |
| 🛡️ Risco de Fraude | Alto (Manipulação manual) | Zero (Regras codificadas) |
| 🔍 Acurácia | ~95% (humano erra) | 100% (máquina não erra) |

---

## 🏗️ Arquitetura de Dados (Medallion Architecture)

O projeto foi estruturado seguindo as **melhores práticas de governança de dados** do mercado:

```
┌──────────────────────────────────────────────────────────────┐
│ Sistemas de Origem (CSV)                                     │
│ Vendas da Operadora + Extratos Bancários                    │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │ 🥉 Camada Bronze (Raw)              │
        │ • Ingestão em formato CSV           │
        │ • Sem transformação                 │
        │ • Storage: data/bronze/             │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │ 🥈 Camada Silver (Cleaned)          │
        │ • Limpeza e tipagem estrita         │
        │ • Tratamento de nulos               │
        │ • Mascaramento LGPD de CPFs         │
        │ • Storage: Parquet (colunar)        │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │ 🥇 Camada Gold (Analytical)         │
        │ • Regras de negócio                 │
        │ • Join de conciliação               │
        │ • Cálculo de divergências           │
        │ • Storage: Parquet (final)          │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │ 📊 Dashboard Streamlit              │
        │ • KPIs em tempo real                │
        │ • Filtros por CPF, data, status     │
        │ • Auditoria Executiva               │
        └─────────────────────────────────────┘
```

### Componentes Principais

1. **Camada Bronze (Raw):** Ingestão e armazenamento dos arquivos brutos em formato CSV.
2. **Camada Silver (Cleaned):** Limpeza de dados, tipagem estrita, tratamento de nulos e mascaramento de dados sensíveis (LGPD) salvos em formato colunar Parquet.
3. **Camada Gold (Analytical):** Processamento das regras de negócio, join de reconciliação e cruzamento analítico gerando o dataset final para análise.

---

## 🛠️ Stack Tecnológica

| Ferramenta | Versão | Propósito |
|-----------|--------|----------|
| **Python** | 3.11 | Linguagem base para ETL |
| **DuckDB** | 1.0.0 | Engine OLAP de alta performance |
| **Pandas** | 2.0.0 | Manipulação de DataFrames |
| **PyArrow** | 14.0.0 | Formato Parquet otimizado |
| **Streamlit** | 1.30.0 | Dashboard interativo |
| **Pytest** | 7.4.0 | Testes unitários |
| **Black** | 23.7.0 | Formatação de código |
| **Flake8** | 6.0.0 | Linting e qualidade |

---

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- Git
- Pip

### 1. Clonar o Repositório

```bash
git clone https://github.com/Sharkduh/auditoria_bancaria.git
cd auditoria_bancaria
```

### 2. Configurar Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o Pipeline Completo

Opção A - Usando Makefile (Recomendado):

```bash
make setup      # Configura ambiente
make bronze     # Gera dados brutos
make silver     # Limpa e processa
make gold       # Aplica regras de negócio
make run        # Inicia dashboard
```

Opção B - Executar manualmente:

```bash
# Passo 1: Gerar a base de dados bruta (Camada Bronze)
python scripts/gerador_dados.py

# Passo 2: Executar a limpeza e mascaramento (Camada Silver)
python scripts/processamento_silver.py

# Passo 3: Aplicar regras de negócio (Camada Gold)
python scripts/conciliacao_gold.py

# Passo 4: Iniciar o painel de auditoria
streamlit run scripts/app_dashboard.py
```

### 5. Executar Testes

```bash
make test
# ou
pytest tests/ -v
```

---

## 📁 Estrutura do Projeto

```
auditoria_bancaria/
├── .github/
│   └── workflows/
│       └── tests.yml              # CI/CD Pipeline (GitHub Actions)
├── scripts/
│   ├── gerador_dados.py           # Gera dados simulados (Bronze)
│   ├── processamento_silver.py    # Limpeza e tipagem (Silver)
│   ├── conciliacao_gold.py        # Regras de negócio (Gold)
│   └── app_dashboard.py           # Dashboard Streamlit
├── tests/
│   ├── test_bronze.py             # Testes da camada Bronze
│   ├── test_silver.py             # Testes da camada Silver
│   └── test_gold.py               # Testes da camada Gold
├── data/
│   ├── bronze/                    # Dados brutos (CSV)
│   ├── silver/                    # Dados processados (Parquet)
│   └── gold/                      # Dados finais (Parquet)
├── Makefile                       # Automação de comandos
├── requirements.txt               # Dependências Python
├── .env.example                   # Variáveis de ambiente
├── .gitignore                     # Arquivos ignorados
├── LICENSE                        # MIT License
├── README.md                      # Este arquivo
├── ARCHITECTURE.md                # Documentação técnica
├── DATA_DICTIONARY.md             # Dicionário de dados
├── CONTRIBUTING.md                # Guia de contribuição
└── RESULTS.md                     # Resultados e análises

```

---

## 🔐 Segurança & Conformidade

### LGPD (Lei Geral de Proteção de Dados)
- ✅ CPFs são mascarados na transição Bronze → Silver
- ✅ Formato: `***123***00` (apenas últimos 2 dígitos visíveis)
- ✅ Impossível recuperar CPF original a partir da camada Silver

### Proteção contra SQL Injection
- ✅ Uso de máscaras booleanas no Pandas (sem concatenação SQL)
- ✅ Filtros dinâmicos sem risco de injeção
- ✅ Queries DuckDB parametrizadas

### Performance & Caching
- ✅ `@st.cache_data` evita leituras redundantes de disco
- ✅ Formato Parquet otimizado em colunas
- ✅ DuckDB OLAP processa milhões de linhas em ms

---

## 📊 Exemplo de Uso

```python
import duckdb
import pandas as pd

# Conectar ao DuckDB
conn = duckdb.connect('data/gold/conciliacao_final.parquet')

# Query: Listar divergências
query = """
    SELECT 
        id_transacao,
        client_cpf,
        valor_liquido_operadora,
        valor_liquido_banco,
        diferenca_conciliacao
    FROM 'data/gold/conciliacao_final.parquet'
    WHERE status_conciliacao = 'Divergente'
    ORDER BY diferenca_conciliacao DESC
    LIMIT 10
"""

result = conn.execute(query).fetchall()
df = pd.DataFrame(result)
print(df)
```

---

## 🧪 Testes

O projeto inclui testes automatizados para cada camada:

```bash
# Executar todos os testes
pytest tests/ -v

# Executar teste específico
pytest tests/test_gold.py -v

# Com coverage
pytest tests/ --cov=scripts --cov-report=html
```

---

## 📈 Resultados Esperados

Após executar o pipeline completo, você verá:

1. **Dashboard Streamlit** com:
   - KPI de transações conciliadas vs. divergentes
   - Filtros por CPF, período e status
   - Gráficos de distribuição de divergências
   - Relatório detalhado de vazamento de receita

2. **Arquivos Parquet** gerados em:
   - `data/silver/silver_operadora.parquet` (~10k registros)
   - `data/gold/conciliacao_final.parquet` (resultado final)

3. **Logs** com detalhes de processamento em cada etapa

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre nosso código de conduta e processo de submissão.

### Passos Rápidos:
1. Faça um Fork do repositório
2. Crie uma branch (`git checkout -b feature/sua-feature`)
3. Commit com mensagens semânticas (`feat:`, `fix:`, `docs:`)
4. Push para a branch (`git push origin feature/sua-feature`)
5. Abra um Pull Request

---

## 📚 Documentação Adicional

- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada do projeto
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) - Esquema de dados por camada
- [RESULTS.md](RESULTS.md) - Análises e impacto de negócio
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guia de contribuição

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💼 Autor

**Eduardo dos Santos Miranda**
- 🔗 LinkedIn: [linkedin.com/in/eduardodossantosmiranda](https://www.linkedin.com/in/eduardodossantosmiranda)
- 🐙 GitHub: [@Sharkduh](https://github.com/Sharkduh)

---

## 🙏 Agradecimentos

- FIAP pela formação em Análise de Dados
- Comunidade Python por ferramentas incríveis (DuckDB, Pandas, Streamlit)
- Recrutadores que apreciam bom código e documentação! 🚀

---

**Última atualização:** Junho 2026 | **Status:** ✅ Produção
