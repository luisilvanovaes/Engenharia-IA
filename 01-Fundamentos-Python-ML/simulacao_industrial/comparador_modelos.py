
"""Treinamento comparativo de classificadores de falhas industriais."""

import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from simulacao_industrial.classificador_falhas import (
    treinar_regressao_logistica,
)


def treinar_tres_estimadores(
    X_treino: pd.DataFrame,
    y_treino: pd.Series,
) -> dict:
    """
    Treina três classificadores utilizando o mesmo conjunto de dados.

    Modelos:
    - Regressão Logística;
    - Árvore de Decisão;
    - Random Forest.

    A divisão temporal deve ser realizada antes desta função.
    """

    if len(X_treino) != len(y_treino):
        raise ValueError(
            "X_treino e y_treino devem ter o mesmo tamanho."
        )

    if len(X_treino) == 0:
        raise ValueError(
            "O conjunto de treinamento não pode estar vazio."
        )

    if y_treino.nunique() < 2:
        raise ValueError(
            "O treinamento exige exemplos das duas classes."
        )

    regressao_logistica = treinar_regressao_logistica(
        X_treino,
        y_treino,
    )

    arvore_decisao = DecisionTreeClassifier(
        max_depth=4,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
    )

    arvore_decisao.fit(X_treino, y_treino)

    random_forest = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    random_forest.fit(X_treino, y_treino)

    return {
        "Regressão Logística": regressao_logistica,
        "Árvore de Decisão": arvore_decisao,
        "Random Forest": random_forest,
    }
