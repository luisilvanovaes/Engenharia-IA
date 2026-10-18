from pathlib import Path

import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from exercicios.integridade_qualidade import calcular_sha256_artefato


RAIZ_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_DADOS = RAIZ_PROJETO / "dados" / "consumo_energetico_v1.csv"

app = FastAPI(
    title="AI Energy Auditor",
    description="Protótipo de auditoria energética com IA",
    version="0.1.0",
)


class EntradaPrevisao(BaseModel):
    horas_operacao: float = Field(..., gt=0, le=24)


def carregar_dados():
    dados = pd.read_csv(ARQUIVO_DADOS)

    colunas = {"data", "horas_operacao", "consumo_kwh"}

    if not colunas.issubset(dados.columns):
        raise ValueError("Colunas obrigatórias ausentes.")

    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="raise"
    )

    return dados.sort_values("data").reset_index(drop=True)


def treinar_modelo_ridge():
    dados = carregar_dados()

    treino = dados.iloc[:23]

    pipeline = Pipeline([
        (
            "preprocessamento",
            ColumnTransformer([
                (
                    "padronizacao",
                    StandardScaler(),
                    ["horas_operacao"]
                )
            ])
        ),
        ("modelo", Ridge(alpha=0.01))
    ])

    pipeline.fit(
        treino[["horas_operacao"]],
        treino["consumo_kwh"]
    )

    return pipeline


modelo_ridge = treinar_modelo_ridge()


@app.get("/")
def pagina_inicial():
    return {
        "sistema": "AI Energy Auditor",
        "versao": "0.1.0",
        "status": "em desenvolvimento"
    }


@app.get("/health")
def verificar_saude():
    return {
        "status": "ok",
        "servico": "AI Energy Auditor"
    }


@app.get("/dados/resumo")
def resumo_energetico():
    dados = carregar_dados()

    return {
        "total_registros": int(len(dados)),
        "consumo_total_kwh": round(
            float(dados["consumo_kwh"].sum()), 4
        ),
        "consumo_medio_kwh": round(
            float(dados["consumo_kwh"].mean()), 4
        ),
        "horas_operacao_total": int(
            dados["horas_operacao"].sum()
        )
    }


@app.get("/dados/integridade")
def integridade_dados():
    try:
        hash_sha256 = calcular_sha256_artefato(
            ARQUIVO_DADOS
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Arquivo de dados não encontrado."
        )

    return {
        "arquivo": ARQUIVO_DADOS.name,
        "algoritmo": "SHA-256",
        "sha256": hash_sha256
    }


@app.post("/previsao")
def prever_consumo(entrada: EntradaPrevisao):
    dados_entrada = pd.DataFrame({
        "horas_operacao": [entrada.horas_operacao]
    })

    previsao = float(
        modelo_ridge.predict(dados_entrada)[0]
    )

    if not np.isfinite(previsao):
        raise HTTPException(
            status_code=500,
            detail="Previsão numérica inválida."
        )

    return {
        "modelo": "Ridge",
        "horas_operacao": entrada.horas_operacao,
        "consumo_previsto_kwh": round(previsao, 4),
        "unidade": "kWh"
    }


# EXERCICIO 73 - ENDPOINT DE ANOMALIAS

@app.get("/anomalias")
def consultar_anomalias():
    from sklearn.ensemble import IsolationForest
    from sklearn.neighbors import LocalOutlierFactor

    dados = carregar_dados()
    variaveis = dados[["horas_operacao", "consumo_kwh"]]

    # Isolation Forest
    detector_isolation = Pipeline([
        ("padronizacao", StandardScaler()),
        (
            "detector",
            IsolationForest(
                n_estimators=100,
                contamination=0.10,
                random_state=42
            )
        )
    ])

    rotulos_isolation = detector_isolation.fit_predict(
        variaveis
    )

    dados["possivel_anomalia"] = (
        rotulos_isolation == -1
    )

    # Regra IQR para consumo por hora
    dados["kwh_por_hora"] = (
        dados["consumo_kwh"] / dados["horas_operacao"]
    )

    q1 = dados["kwh_por_hora"].quantile(0.25)
    q3 = dados["kwh_por_hora"].quantile(0.75)
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    dados["anomalia_regra"] = (
        (dados["kwh_por_hora"] < limite_inferior)
        | (dados["kwh_por_hora"] > limite_superior)
    )

    # Local Outlier Factor
    dados_padronizados = StandardScaler().fit_transform(
        variaveis
    )

    detector_lof = LocalOutlierFactor(
        n_neighbors=5,
        contamination=0.10
    )

    dados["anomalia_lof"] = (
        detector_lof.fit_predict(dados_padronizados) == -1
    )

    # Consolidacao dos alertas
    colunas_alertas = [
        "possivel_anomalia",
        "anomalia_regra",
        "anomalia_lof"
    ]

    dados["total_alertas"] = (
        dados[colunas_alertas].sum(axis=1)
    )

    fila = dados.loc[
        dados["total_alertas"] > 0
    ].copy()

    fila = fila.sort_values(
        ["total_alertas", "data"],
        ascending=[False, True]
    )

    alertas = []

    for _, registro in fila.iterrows():
        metodos = []

        if registro["possivel_anomalia"]:
            metodos.append("Isolation Forest")

        if registro["anomalia_regra"]:
            metodos.append("IQR")

        if registro["anomalia_lof"]:
            metodos.append("LOF")

        prioridade = (
            "Alta - investigar"
            if registro["total_alertas"] >= 2
            else "Revisao - verificar"
        )

        alertas.append({
            "data": registro["data"].strftime("%Y-%m-%d"),
            "horas_operacao": int(
                registro["horas_operacao"]
            ),
            "consumo_kwh": round(
                float(registro["consumo_kwh"]), 4
            ),
            "total_alertas": int(
                registro["total_alertas"]
            ),
            "prioridade": prioridade,
            "metodos": metodos
        })

    return {
        "total_registros_analisados": len(dados),
        "total_registros_sinalizados": len(alertas),
        "alertas": alertas,
        "observacao": (
            "Alertas estatisticos nao comprovam "
            "fraude ou desperdicio energetico."
        )
    }
