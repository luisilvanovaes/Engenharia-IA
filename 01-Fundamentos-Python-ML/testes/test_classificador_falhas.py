"""Testes automatizados do classificador de falhas industriais."""

import pytest

from simulacao_industrial.gerador_dados import gerar_dados_industriais
from simulacao_industrial.classificador_falhas import (
    preparar_dados_classificacao,
    dividir_dados_temporais,
    treinar_regressao_logistica,
    avaliar_classificador,
)


@pytest.fixture
def dados_classificacao():
    """Prepara dados industriais simulados para os testes."""
    dados = gerar_dados_industriais()
    X, y = preparar_dados_classificacao(dados)
    return dividir_dados_temporais(X, y)


def test_treinamento_classificador(dados_classificacao):
    """Verifica o treinamento com dados válidos."""
    partes = dados_classificacao

    modelo = treinar_regressao_logistica(
        partes["X_treino"],
        partes["y_treino"],
    )

    assert modelo.named_steps["classificador"].n_features_in_ == 7
    assert list(modelo.classes_) == [0, 1]


def test_avaliacao_classificador(dados_classificacao):
    """Verifica métricas e custo financeiro da avaliação."""
    partes = dados_classificacao

    modelo = treinar_regressao_logistica(
        partes["X_treino"],
        partes["y_treino"],
    )

    resultados = avaliar_classificador(
        modelo,
        partes["X_validacao"],
        partes["y_validacao"],
    )

    assert 0 <= resultados["acuracia"] <= 1
    assert 0 <= resultados["precisao"] <= 1
    assert 0 <= resultados["recall"] <= 1
    assert resultados["custo_financeiro"] >= 0

    total = (
        resultados["verdadeiros_negativos"]
        + resultados["falsos_positivos"]
        + resultados["falsos_negativos"]
        + resultados["verdadeiros_positivos"]
    )

    assert total == len(partes["y_validacao"])


def test_limiar_invalido(dados_classificacao):
    """Rejeita um limiar de classificação fora do intervalo."""
    partes = dados_classificacao

    modelo = treinar_regressao_logistica(
        partes["X_treino"],
        partes["y_treino"],
    )

    with pytest.raises(ValueError):
        avaliar_classificador(
            modelo,
            partes["X_validacao"],
            partes["y_validacao"],
            limiar=1.5,
        )