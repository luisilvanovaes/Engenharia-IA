"""Ajuste de hiperparâmetros com validação temporal."""

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit


def ajustar_random_forest(
    X_treino: pd.DataFrame,
    y_treino: pd.Series,
    n_iter: int = 10,
    n_splits: int = 3,
) -> RandomizedSearchCV:
    """
    Ajusta uma Random Forest usando validação cruzada temporal.

    Utiliza exclusivamente os dados de treinamento.
    Os conjuntos externos de validação e teste não são utilizados.
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

    if n_iter < 1:
        raise ValueError(
            "n_iter deve ser maior ou igual a 1."
        )

    if n_splits < 2 or n_splits >= len(X_treino):
        raise ValueError(
            "n_splits deve ser pelo menos 2 e menor que "
            "a quantidade de registros."
        )

    modelo = RandomForestClassifier(
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    parametros = {
        "n_estimators": [50, 100, 150],
        "max_depth": [3, 4, 6, 8, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 3, 5],
        "max_features": ["sqrt", "log2"],
    }

    validacao_temporal = TimeSeriesSplit(
        n_splits=n_splits,
    )

    busca = RandomizedSearchCV(
        estimator=modelo,
        param_distributions=parametros,
        n_iter=n_iter,
        scoring="recall",
        cv=validacao_temporal,
        random_state=42,
        n_jobs=-1,
        refit=True,
        error_score="raise",
    )

    busca.fit(X_treino, y_treino)

    return busca