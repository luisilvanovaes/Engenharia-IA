"""Testes dos custos financeiros de falhas industriais."""

import pytest

from simulacao_industrial.custos_falhas import calcular_custo_falhas


def test_custo_cenario_tipico():
    """Valida o cálculo com falsos positivos e negativos."""
    resultado = calcular_custo_falhas(3, 2)

    assert resultado == 4450.0


def test_custo_sem_erros():
    """Sem erros de classificação, o custo deve ser zero."""
    assert calcular_custo_falhas(0, 0) == 0.0


def test_custo_personalizado():
    """Permite configurar custos específicos da fábrica."""
    resultado = calcular_custo_falhas(
        falsos_positivos=2,
        falsos_negativos=1,
        custo_falso_positivo=300.0,
        custo_falso_negativo=5000.0,
    )

    assert resultado == 5600.0


def test_quantidade_negativa_invalida():
    """Não aceita quantidades negativas de erros."""
    with pytest.raises(ValueError):
        calcular_custo_falhas(-1, 2)


def test_custo_financeiro_negativo_invalido():
    """Não aceita custos financeiros negativos."""
    with pytest.raises(ValueError):
        calcular_custo_falhas(
            1,
            1,
            custo_falso_negativo=-2000.0,
        )