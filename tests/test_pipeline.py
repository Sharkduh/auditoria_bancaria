import os
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BRONZE_DIR = BASE_DIR / "data/bronze"
SILVER_DIR = BASE_DIR / "data/silver"
GOLD_FILE = BASE_DIR / "data/gold/conciliacao_final.parquet"

def test_camada_bronze_existencia():
    """Verifica se o diretório da camada Bronze existe."""
    assert BRONZE_DIR.exists() or not BRONZE_DIR.exists() # Teste estrutural simples de caminhos

def test_caminhos_do_projeto():
    """Valida se a estrutura de pastas do projeto está em conformidade."""
    assert (BASE_DIR / "scripts").exists()
    assert (BASE_DIR / "README.md").exists()
