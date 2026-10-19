"""Testes do ajuste de hiperparâmetros com validação temporal."""

import pandas as pd
import pytest

from simulacao_industrial.gerador_dados import gerar_dados_industriais
from simulacao_industrial.classificador_falhas import (
    preparar_dados_classificacao,
    dividir_dados_temporais,
)
from simulacao_industrial.ajuste_hiperparametros import (
    ajustar_random_forest,
)


@pytest.fixture
def dados_treinamento():
    """Prepara dados simulados com divisão cronológica."""
    dados = gerar_dados_industriais()

    X, y = preparar_dados_classificacao(dados)

    conjuntos = dividir_dados_temporais(X, y)

    return conjuntos["X_treino"], conjuntos["y_treino"]


def test_ajuste_random_forest_caso_tipico(dados_treinamento):
    """Verifica o ajuste em um cenário válido."""
    X_treino, y_treino = dados_treinamento

    busca = ajustar_random_forest(
        X_treino,
        y_treino,
        n_iter=2,
        n_splits=3,
    )

    assert busca.best_estimator_ is not None
    assert len(busca.cv_results_["params"]) == 2
    assert 0.0 <= busca.best_score_ <= 1.0


def test_ajuste_rejeita_conjunto_vazio():
    """Verifica a rejeição de treinamento sem registros."""
    X_treino = pd.DataFrame()
    y_treino = pd.Series(dtype=int)

    with pytest.raises(ValueError, match="vazio"):
        ajustar_random_forest(X_treino, y_treino)


def test_ajuste_rejeita_tamanhos_incompativeis(
    dados_treinamento,
):
    """Verifica a rejeição de entradas com tamanhos diferentes."""
    X_treino, y_treino = dados_treinamento

    with pytest.raises(ValueError, match="mesmo tamanho"):
        ajustar_random_forest(
            X_treino.iloc[:-1],
            y_treino,
        )


def test_ajuste_rejeita_iteracoes_invalidas(
    dados_treinamento,
):
    """Verifica a rejeição de n_iter igual a zero."""
    X_treino, y_treino = dados_treinamento

    with pytest.raises(ValueError, match="n_iter"):
        ajustar_random_forest(
            X_treino,
            y_treino,
            n_iter=0,
        )