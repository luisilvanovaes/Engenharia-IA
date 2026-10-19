
"""Testes automatizados do relatório comparativo de modelos."""

import pandas as pd
import pytest

from simulacao_industrial.relatorio_comparador import (
    gerar_relatorio_comparativo,
)


@pytest.fixture(scope="module")
def relatorio():
    """Executa o comparador uma vez para os testes válidos."""
    return gerar_relatorio_comparativo(
        dias=365,
        semente=42,
        n_iter=2,
    )


def test_relatorio_cenario_tipico(relatorio):
    """Verifica a estrutura e os quatro classificadores."""

    assert isinstance(relatorio, pd.DataFrame)
    assert len(relatorio) == 4

    modelos_esperados = {
        "Regressão Logística",
        "Árvore de Decisão",
        "Random Forest",
        "Random Forest otimizada",
    }

    assert set(relatorio["modelo"]) == modelos_esperados

    colunas_esperadas = {
        "modelo",
        "acuracia",
        "precisao",
        "recall",
        "falsos_positivos",
        "falsos_negativos",
        "custo_financeiro",
    }

    assert colunas_esperadas.issubset(relatorio.columns)

    # Verificar se todas as métricas estão entre 0 e 1.
    metricas = relatorio[
        ["acuracia", "precisao", "recall"]
    ]

    valores_validos = (
        (metricas >= 0) & (metricas <= 1)
    ).to_numpy().all()

    assert bool(valores_validos)


def test_relatorio_ordenado_por_custo(relatorio):
    """Verifica se o menor custo financeiro aparece primeiro."""

    custos = relatorio["custo_financeiro"].tolist()

    assert custos == sorted(custos)

    # Converter explicitamente para um booleano.
    custos_validos = (
        relatorio["custo_financeiro"]
        .ge(0)
        .to_numpy()
        .all()
    )

    assert bool(custos_validos)


def test_relatorio_rejeita_iteracoes_invalidas():
    """Verifica a rejeição de n_iter igual a zero."""

    with pytest.raises(ValueError, match="n_iter"):
        gerar_relatorio_comparativo(
            dias=365,
            semente=42,
            n_iter=0,
        )
