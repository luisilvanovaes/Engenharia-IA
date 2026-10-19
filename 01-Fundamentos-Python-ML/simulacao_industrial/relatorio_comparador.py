"""Relatório comparativo de classificadores de falhas industriais."""

import pandas as pd

from simulacao_industrial.gerador_dados import (
    gerar_dados_industriais,
)
from simulacao_industrial.classificador_falhas import (
    preparar_dados_classificacao,
    dividir_dados_temporais,
    avaliar_classificador,
)
from simulacao_industrial.comparador_modelos import (
    treinar_tres_estimadores,
)
from simulacao_industrial.ajuste_hiperparametros import (
    ajustar_random_forest,
)


def gerar_relatorio_comparativo(
    dias: int = 365,
    semente: int = 42,
    n_iter: int = 10,
) -> pd.DataFrame:
    """
    Compara quatro classificadores de falhas industriais.

    O treinamento e a busca de hiperparâmetros utilizam
    exclusivamente o conjunto de treinamento.

    A avaliação utiliza o conjunto externo de validação.
    O conjunto de teste permanece reservado.
    """

    dados = gerar_dados_industriais(
        dias=dias,
        semente=semente,
    )

    X, y = preparar_dados_classificacao(dados)

    conjuntos = dividir_dados_temporais(X, y)

    X_treino = conjuntos["X_treino"]
    y_treino = conjuntos["y_treino"]

    X_validacao = conjuntos["X_validacao"]
    y_validacao = conjuntos["y_validacao"]

    modelos = treinar_tres_estimadores(
        X_treino,
        y_treino,
    )

    busca = ajustar_random_forest(
        X_treino,
        y_treino,
        n_iter=n_iter,
        n_splits=3,
    )

    modelos["Random Forest otimizada"] = (
        busca.best_estimator_
    )

    resultados = []

    for nome, modelo in modelos.items():
        metricas = avaliar_classificador(
            modelo,
            X_validacao,
            y_validacao,
        )

        resultados.append({
            "modelo": nome,
            "acuracia": metricas["acuracia"],
            "precisao": metricas["precisao"],
            "recall": metricas["recall"],
            "falsos_positivos": metricas[
                "falsos_positivos"
            ],
            "falsos_negativos": metricas[
                "falsos_negativos"
            ],
            "custo_financeiro": metricas[
                "custo_financeiro"
            ],
        })

    relatorio = pd.DataFrame(resultados)

    relatorio = relatorio.sort_values(
        by=[
            "custo_financeiro",
            "falsos_negativos",
            "falsos_positivos",
        ],
        ascending=True,
    ).reset_index(drop=True)

    return relatorio