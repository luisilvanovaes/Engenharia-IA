"""Testes automatizados do simulador industrial."""

import numpy as np
import pytest

from simulacao_industrial.gerador_dados import gerar_dados_industriais


@pytest.fixture
def dados():
    """Gera uma base reutilizável para os testes."""
    return gerar_dados_industriais()


def test_quantidade_registros(dados):
    assert len(dados) == 365


def test_datas_sem_duplicacao(dados):
    assert not dados["data"].duplicated().any()


def test_turnos_validos(dados):
    assert dados["turnos_planejados"].between(1, 3).all()


def test_horas_operacao_validas(dados):
    assert dados["horas_operacao"].between(0, 24).all()


def test_producao_nao_negativa(dados):
    assert (dados["producao_unidades"] >= 0).all()


def test_consumo_nao_negativo(dados):
    assert (dados["consumo_kwh"] >= 0).all()


def test_reprodutibilidade():
    a = gerar_dados_industriais(semente=42)
    b = gerar_dados_industriais(semente=42)

    assert a.equals(b)


def test_consumo_dia_anterior(dados):
    esperado = dados["consumo_kwh"].shift(1)

    assert np.allclose(
        dados["consumo_kwh_dia_anterior"],
        esperado,
        equal_nan=True,
    )


def test_media_movel_sem_vazamento(dados):
    esperado = (
        dados["consumo_kwh"]
        .shift(1)
        .rolling(window=7, min_periods=7)
        .mean()
        .round(2)
    )

    assert np.allclose(
        dados["media_consumo_7d"],
        esperado,
        equal_nan=True,
    )

def test_dias_invalidos():
    with pytest.raises(ValueError):
        gerar_dados_industriais(dias=0)

def test_classificacao_falhas_binaria(dados):
    """O rótulo de falha deve ser binário."""
    assert dados["falha_operacional"].isin([0, 1]).all()


def test_classificacao_falhas_duas_classes(dados):
    """A base padrão deve conter dias normais e com falhas."""
    classes = set(dados["falha_operacional"].unique())

    assert classes == {0, 1}


def test_simulacao_falhas_um_dia():
    """A simulação deve funcionar mesmo com um único registro."""
    dados = gerar_dados_industriais(dias=1)

    assert len(dados) == 1
    assert dados["falha_operacional"].iloc[0] in (0, 1)
    assert dados["consumo_kwh"].iloc[0] >= 0