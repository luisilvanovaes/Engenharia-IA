"""Testes automatizados do comparador de modelos industriais."""

import pytest

from simulacao_industrial.gerador_dados import gerar_dados_industriais
from simulacao_industrial.classificador_falhas import (
    preparar_dados_classificacao,
    dividir_dados_temporais,
)
from simulacao_industrial.comparador_modelos import treinar_tres_estimadores


@pytest.fixture
def dados_treinamento():
    """Prepara dados sintéticos com divisão temporal."""
    dados = gerar_dados_industriais()
    X, y = preparar_dados_classificacao(dados)
    divisao = dividir_dados_temporais(X, y)

    return divisao["X_treino"], divisao["y_treino"]


def test_treina_tres_estimadores(dados_treinamento):
    """Caso típico: os três modelos devem ser treinados."""
    X_treino, y_treino = dados_treinamento

    modelos = treinar_tres_estimadores(X_treino, y_treino)

    assert len(modelos) == 3

    assert set(modelos.keys()) == {
        "Regressão Logística",
        "Árvore de Decisão",
        "Random Forest",
    }

    for modelo in modelos.values():
        previsoes = modelo.predict(X_treino)

        assert len(previsoes) == len(y_treino)
        assert set(previsoes).issubset({0, 1})


def test_rejeita_treinamento_vazio(dados_treinamento):
    """Caso extremo: conjuntos vazios devem ser rejeitados."""
    X_treino, y_treino = dados_treinamento

    with pytest.raises(ValueError, match="não pode estar vazio"):
        treinar_tres_estimadores(
            X_treino.iloc[:0],
            y_treino.iloc[:0],
        )


def test_rejeita_tamanhos_diferentes(dados_treinamento):
    """Caso inválido: entradas e alvos com tamanhos distintos."""
    X_treino, y_treino = dados_treinamento

    with pytest.raises(ValueError, match="mesmo tamanho"):
        treinar_tres_estimadores(
            X_treino,
            y_treino.iloc[:-1],
        )


def test_rejeita_apenas_uma_classe(dados_treinamento):
    """Caso inválido: treinamento sem exemplos das duas classes."""
    X_treino, y_treino = dados_treinamento

    indices_normais = y_treino[y_treino == 0].index

    with pytest.raises(ValueError, match="duas classes"):
        treinar_tres_estimadores(
            X_treino.loc[indices_normais],
            y_treino.loc[indices_normais],
        )