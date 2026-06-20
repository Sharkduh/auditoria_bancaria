.PHONY: setup run test clean bronze silver gold dashboard

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

bronze:
	.venv/bin/python scripts/gerador_dados.py

silver:
	.venv/bin/python scripts/processamento_silver.py

gold:
	.venv/bin/python scripts/conciliacao_gold.py

run:
	.venv/bin/streamlit run scripts/app_dashboard.py

test:
	.venv/bin/pytest tests/
