
# Exercício 35 — Etapa 1
# Teste automatizado de integridade do dataset

import json
import hashlib
from pathlib import Path
import pandas as pd

# Localizar a raiz do projeto
PROJETO = Path(__file__).resolve().parents[1]


def test_integridade_sha256():

    # Carregar o manifesto
    caminho_manifesto = (
        PROJETO / "resultados" / "exercicio34_manifesto.json"
    )

    with caminho_manifesto.open(
        "r", encoding="utf-8"
    ) as arquivo:
        manifesto = json.load(arquivo)

    # Localizar o dataset
    caminho_csv = PROJETO / manifesto["arquivo_dados"]

    # Calcular o hash atual
    hash_atual = hashlib.sha256(
        caminho_csv.read_bytes()
    ).hexdigest()

    # Comparar com a referência registrada
    assert hash_atual == manifesto["sha256_dados"]


def test_estrutura_dataset():

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    colunas_esperadas = [
        "data",
        "horas_operacao",
        "consumo_kwh"
    ]

    assert list(dados.columns) == colunas_esperadas
    assert len(dados) == 30


def test_ausencia_valores_nulos():

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    assert not dados.isnull().values.any()


# ============================================================
# EXERCÍCIO 35 — ETAPA 3
# Testes de regras de negócio
# ============================================================

def test_horas_operacao():

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    assert dados["horas_operacao"].between(6, 12).all()


def test_consumo_positivo():

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    assert (dados["consumo_kwh"] > 0).all()


def test_datas_unicas():

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    datas = pd.to_datetime(
        dados["data"],
        format="%Y-%m-%d",
        errors="raise"
    )

    assert datas.is_unique
    assert datas.is_monotonic_increasing

    intervalos = datas.diff().dropna()
    assert (intervalos == pd.Timedelta(days=1)).all()


# ============================================================
# EXERCÍCIO 35 — ETAPA 4
# Testes negativos com dados inválidos
# ============================================================

def validar_horas_operacao(dados):

    if not dados["horas_operacao"].between(6, 12).all():
        raise ValueError(
            "Horas de operação fora do intervalo permitido."
        )


def test_rejeitar_horas_invalidas():

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    # Criar uma cópia para não alterar o dataset original
    dados_invalidos = dados.copy()

    # Simular um valor impossível para este experimento
    dados_invalidos.loc[0, "horas_operacao"] = 25

    # Verificar se a validação rejeita os dados
    import pytest

    with pytest.raises(ValueError):
        validar_horas_operacao(dados_invalidos)


# ============================================================
# EXERCÍCIO 35 — ETAPA 5
# Teste negativo: horas de operação ausentes
# ============================================================

def test_rejeitar_horas_ausentes():

    import pytest
    import numpy as np

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    # Criar uma cópia dos dados originais
    dados_invalidos = dados.copy()

    # Simular uma medição ausente
    dados_invalidos.loc[0, "horas_operacao"] = np.nan

    # A função deve rejeitar os dados inválidos
    with pytest.raises(ValueError):
        validar_horas_operacao(dados_invalidos)


# ============================================================
# EXERCÍCIO 35 — ETAPA 6
# Testes negativos de consumo energético
# ============================================================

def validar_consumo_energetico(dados):

    if not (dados["consumo_kwh"] > 0).all():
        raise ValueError(
            "Consumo energético inválido ou ausente."
        )


def test_rejeitar_consumo_negativo():

    import pytest

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    # Criar uma cópia dos dados
    dados_invalidos = dados.copy()

    # Simular consumo negativo
    dados_invalidos.loc[0, "consumo_kwh"] = -50

    # Confirmar que a validação rejeita o valor
    with pytest.raises(
        ValueError,
        match="Consumo energético inválido"
    ):
        validar_consumo_energetico(dados_invalidos)


def test_rejeitar_consumo_zero():

    import pytest

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    # Criar uma cópia dos dados
    dados_invalidos = dados.copy()

    # Simular consumo igual a zero
    dados_invalidos.loc[0, "consumo_kwh"] = 0

    # Confirmar que a validação rejeita o valor
    with pytest.raises(
        ValueError,
        match="Consumo energético inválido"
    ):
        validar_consumo_energetico(dados_invalidos)


# ============================================================
# EXERCÍCIO 35 — ETAPA 7
# Teste negativo: consumo energético ausente
# ============================================================

def test_rejeitar_consumo_ausente():

    import pytest
    import numpy as np

    caminho_csv = (
        PROJETO / "dados" / "consumo_energetico_v1.csv"
    )

    dados = pd.read_csv(caminho_csv)

    # Criar uma cópia para preservar o dataset original
    dados_invalidos = dados.copy()

    # Simular falha de leitura do medidor
    dados_invalidos.loc[0, "consumo_kwh"] = np.nan

    # A função deve rejeitar a medição ausente
    with pytest.raises(
        ValueError,
        match="Consumo energético inválido"
    ):
        validar_consumo_energetico(dados_invalidos)



