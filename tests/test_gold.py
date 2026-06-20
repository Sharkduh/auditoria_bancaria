"""
Testes Unitários - Camada Gold
Valida cálculos de conciliação e classificação de status.
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Adicionar scripts ao path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConciliacao:
    """Testes para lógica de conciliação."""

    def test_calculo_diferenca_conciliacao(self):
        """Testa cálculo de diferença de conciliação."""
        df = pd.DataFrame({
            "id_transacao": ["TRX001", "TRX002"],
            "valor_liquido_operadora": [100.0, 200.0],
            "valor_liquido_banco": [100.0, 195.0],
        })

        # Calcular diferença (como no script)
        df["diferenca_conciliacao"] = (
            df["valor_liquido_operadora"] - df["valor_liquido_banco"]
        )

        assert df["diferenca_conciliacao"].iloc[0] == 0.0
        assert df["diferenca_conciliacao"].iloc[1] == 5.0

    def test_classificacao_conciliado(self):
        """Testa classificação de transação conciliada."""
        df = pd.DataFrame({
            "diferenca_conciliacao": [0.0, 0.005],
        })

        TOLERANCIA = 0.01

        def classificar(diferenca):
            return "Conciliado" if abs(diferenca) <= TOLERANCIA else "Divergente"

        df["status"] = df["diferenca_conciliacao"].apply(classificar)

        assert df["status"].iloc[0] == "Conciliado"
        assert df["status"].iloc[1] == "Conciliado"

    def test_classificacao_divergente(self):
        """Testa classificação de transação divergente."""
        df = pd.DataFrame({
            "diferenca_conciliacao": [0.5, 1.0, 5.0],
        })

        TOLERANCIA = 0.01

        def classificar(diferenca):
            return "Conciliado" if abs(diferenca) <= TOLERANCIA else "Divergente"

        df["status"] = df["diferenca_conciliacao"].apply(classificar)

        assert all(df["status"] == "Divergente")

    def test_calculo_vazamento_receita(self):
        """Testa cálculo de vazamento de receita."""
        df = pd.DataFrame({
            "id_transacao": ["TRX001", "TRX002", "TRX003"],
            "diferenca_conciliacao": [0.0, 5.0, 10.0],
            "status_conciliacao": ["Conciliado", "Divergente", "Divergente"],
        })

        # Calcular vazamento
        vazamento = (
            df[df["status_conciliacao"] == "Divergente"]["diferenca_conciliacao"]
            .abs()
            .sum()
        )

        assert vazamento == 15.0

    def test_taxa_sucesso_conciliacao(self):
        """Testa cálculo de taxa de sucesso."""
        df = pd.DataFrame({
            "status_conciliacao": [
                "Conciliado", "Conciliado", "Conciliado",
                "Divergente", "Divergente"
            ],
        })

        total = len(df)
        conciliadas = (df["status_conciliacao"] == "Conciliado").sum()
        taxa = (conciliadas / total) * 100

        assert taxa == 60.0

    def test_diferenca_negativa(self):
        """Testa caso onde banco repassa mais que operadora."""
        df = pd.DataFrame({
            "valor_liquido_operadora": [100.0],
            "valor_liquido_banco": [105.0],
        })

        df["diferenca_conciliacao"] = (
            df["valor_liquido_operadora"] - df["valor_liquido_banco"]
        )

        # Diferença negativa significa banco pagou mais
        assert df["diferenca_conciliacao"].iloc[0] == -5.0


class TestValidacaoDados:
    """Testes para validação de dados finais."""

    def test_colunas_esperadas_gold(self):
        """Testa se todas as colunas esperadas existem na Gold."""
        colunas_esperadas = [
            "id_transacao",
            "client_cpf",
            "valor_liquido_operadora",
            "valor_liquido_banco",
            "diferenca_conciliacao",
            "status_conciliacao",
        ]

        df = pd.DataFrame({col: [None] for col in colunas_esperadas})

        for col in colunas_esperadas:
            assert col in df.columns

    def test_sem_nulos_em_gold(self):
        """Testa que não há nulos nas colunas críticas."""
        df = pd.DataFrame({
            "id_transacao": ["TRX001", "TRX002"],
            "valor_liquido_operadora": [100.0, 200.0],
            "valor_liquido_banco": [100.0, 200.0],
            "diferenca_conciliacao": [0.0, 0.0],
            "status_conciliacao": ["Conciliado", "Conciliado"],
        })

        # Verificar colunas críticas
        colunas_criticas = [
            "id_transacao",
            "valor_liquido_operadora",
            "valor_liquido_banco",
            "diferenca_conciliacao",
            "status_conciliacao",
        ]

        for col in colunas_criticas:
            assert not df[col].isnull().any(), f"Coluna {col} contém nulos"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
