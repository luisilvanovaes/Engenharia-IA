"""Gerador de dados industriais simulados para o AI Energy Auditor."""

import numpy as np
import pandas as pd


def gerar_dados_industriais(
    dias: int = 365,
    data_inicio: str = "2025-01-01",
    semente: int = 42,
) -> pd.DataFrame:
    """Prepara um histórico diário reprodutível para uma fábrica virtual."""
    if dias <= 0:
        raise ValueError("O número de dias deve ser maior que zero.")

    rng = np.random.default_rng(semente)
    datas = pd.date_range(start=data_inicio, periods=dias, freq="D")

    df = pd.DataFrame({"data": datas})

    # Planejamento de turnos: menor atividade nos fins de semana
    dia_semana = df["data"].dt.dayofweek

    turnos = np.where(
        dia_semana >= 5,
        1,
        rng.choice([1, 2, 3], size=dias, p=[0.15, 0.55, 0.30])
    )

    df["turnos_planejados"] = turnos.astype(int)

    # Horas efetivas de operação por dia
    horas_planejadas = df["turnos_planejados"] * 8
    variacao_horas = rng.uniform(-1.0, 0.0, size=dias)

    df["horas_operacao"] = np.round(
        np.maximum(1.0, horas_planejadas + variacao_horas),
        2
    )

    # Produção industrial simulada
    produtividade_hora = 45
    variacao_producao = rng.normal(1.0, 0.08, size=dias)

    df["producao_unidades"] = np.maximum(
        0,
        np.round(
            df["horas_operacao"] * produtividade_hora * variacao_producao
        )
    ).astype(int)

    # Temperatura ambiente com sazonalidade anual
    dia_do_ano = df["data"].dt.dayofyear.to_numpy()

    temperatura_sazonal = (
        25
        + 5 * np.cos(2 * np.pi * (dia_do_ano - 15) / 365)
    )

    variacao_temperatura = rng.normal(
        loc=0.0,
        scale=2.0,
        size=dias
    )

    df["temperatura_ambiente_c"] = np.round(
        temperatura_sazonal + variacao_temperatura,
        2
    )

    # Consumo energético industrial simulado
    consumo_fixo = 120.0

    consumo_operacao = (
        df["horas_operacao"] * 18.0
    )

    consumo_producao = (
        df["producao_unidades"] * 0.35
    )

    # Demanda adicional de climatização em dias quentes
    consumo_climatizacao = (
        np.maximum(
            0,
            df["temperatura_ambiente_c"] - 24.0
        ) * 12.0
    )

    # Variação operacional não explicada pelas demais variáveis
    ruido_energetico = rng.normal(
        loc=0.0,
        scale=15.0,
        size=dias
    )

    df["consumo_kwh"] = np.round(
        np.maximum(
            0,
            consumo_fixo
            + consumo_operacao
            + consumo_producao
            + consumo_climatizacao
            + ruido_energetico
        ),
        2
    )

    # Consumo conhecido até o dia anterior
    df["consumo_kwh_dia_anterior"] = (
        df["consumo_kwh"].shift(1)
    )

    # Média do consumo dos sete dias anteriores
    # shift(1) impede o uso do consumo do próprio dia
    df["media_consumo_7d"] = (
        df["consumo_kwh"]
        .shift(1)
        .rolling(window=7, min_periods=7)
        .mean()
        .round(2)
    )

    return df
