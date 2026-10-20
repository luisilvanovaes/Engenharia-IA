"""
Clustering de perfis de consumo industrial.

Semana 04 — Dia 16
AI Energy Auditor

Agrupamento não supervisionado de registros industriais.
"""

VARIAVEIS_CLUSTERING = [
    "horas_operacao",
    "producao_unidades",
    "temperatura_ambiente_c",
    "consumo_kwh",
]

def preparar_dados_clustering(dados):
    """
    Valida e padroniza as variáveis de clustering.

    Parâmetros
    ----------
    dados : pandas.DataFrame
        Registros industriais.

    Retorna
    -------
    tuple
        Matriz padronizada e StandardScaler ajustado.
    """
    import numpy as np
    from sklearn.preprocessing import StandardScaler

    colunas_ausentes = [
        coluna
        for coluna in VARIAVEIS_CLUSTERING
        if coluna not in dados.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {colunas_ausentes}"
        )

    X = dados[VARIAVEIS_CLUSTERING]

    if not all(np.issubdtype(tipo, np.number) for tipo in X.dtypes):
        raise ValueError("As variáveis de clustering devem ser numéricas.")

    if not np.isfinite(X.to_numpy()).all():
        raise ValueError(
            "As variáveis de clustering não podem conter NaN ou infinito."
        )

    escalador = StandardScaler()
    X_padronizado = escalador.fit_transform(X)

    return X_padronizado, escalador

def executar_kmeans(dados, numero_clusters=3):
    """
    Agrupa perfis de consumo industrial utilizando KMeans.

    Parâmetros
    ----------
    dados : pandas.DataFrame
        Registros industriais.
    numero_clusters : int
        Quantidade de agrupamentos desejada.

    Retorna
    -------
    tuple
        DataFrame com os clusters, modelo KMeans e escalador.
    """
    from sklearn.cluster import KMeans

    if (
        isinstance(numero_clusters, bool)
        or not isinstance(numero_clusters, int)
        or numero_clusters < 2
        or numero_clusters > len(dados)
    ):
        raise ValueError(
            "numero_clusters deve ser um inteiro entre 2 "
            "e a quantidade de registros."
        )

    X_padronizado, escalador = preparar_dados_clustering(dados)

    modelo = KMeans(
        n_clusters=numero_clusters,
        random_state=42,
        n_init=10,
    )

    clusters = modelo.fit_predict(X_padronizado)

    resultado = dados.copy()
    resultado["cluster_kmeans"] = clusters

    return resultado, modelo, escalador

def executar_dbscan(dados, eps=0.7, min_samples=5):
    """
    Agrupa registros industriais utilizando DBSCAN.

    O rótulo -1 identifica registros classificados como ruído.
    Ruído não significa, necessariamente, falha ou fraude.
    """
    from sklearn.cluster import DBSCAN
    import math

    if (
        isinstance(eps, bool)
        or not isinstance(eps, (int, float))
        or not math.isfinite(eps)
        or eps <= 0
    ):
        raise ValueError("eps deve ser um número positivo e finito.")

    if (
        isinstance(min_samples, bool)
        or not isinstance(min_samples, int)
        or min_samples < 1
    ):
        raise ValueError("min_samples deve ser um inteiro positivo.")

    X_padronizado, escalador = preparar_dados_clustering(dados)

    modelo = DBSCAN(
        eps=eps,
        min_samples=min_samples,
    )

    clusters = modelo.fit_predict(X_padronizado)

    resultado = dados.copy()
    resultado["cluster_dbscan"] = clusters

    return resultado, modelo, escalador