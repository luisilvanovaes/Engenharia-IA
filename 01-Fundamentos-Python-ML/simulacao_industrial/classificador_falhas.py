"""Preparação de dados para classificação de falhas industriais."""

import pandas as pd


VARIAVEIS_ENTRADA = [
    "turnos_planejados",
    "horas_operacao",
    "producao_unidades",
    "temperatura_ambiente_c",
    "consumo_kwh",
    "consumo_kwh_dia_anterior",
    "media_consumo_7d",
]

VARIAVEL_ALVO = "falha_operacional"


def preparar_dados_classificacao(
    dados: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepara as entradas e o alvo do classificador.

    Os registros sem histórico completo são descartados.
    A ordem cronológica original é preservada.
    """

    colunas_necessarias = VARIAVEIS_ENTRADA + [VARIAVEL_ALVO]

    dados_validos = dados.dropna(
        subset=colunas_necessarias
    ).copy()

    X = dados_validos[VARIAVEIS_ENTRADA].copy()
    y = dados_validos[VARIAVEL_ALVO].copy()

    return X, y

def dividir_dados_temporais(
    X: pd.DataFrame,
    y: pd.Series,
    proporcao_treino: float = 0.70,
    proporcao_validacao: float = 0.15,
) -> dict:
    """
    Divide os dados cronologicamente em treino,
    validação e teste, sem embaralhamento.
    """

    if not 0 < proporcao_treino < 1:
        raise ValueError("Proporção de treino inválida.")

    if not 0 < proporcao_validacao < 1:
        raise ValueError("Proporção de validação inválida.")

    if proporcao_treino + proporcao_validacao >= 1:
        raise ValueError("As proporções devem somar menos que 1.")

    if len(X) != len(y) or not X.index.equals(y.index):
        raise ValueError("X e y devem estar alinhados.")

    n = len(X)

    corte_treino = int(n * proporcao_treino)
    corte_validacao = int(
        n * (proporcao_treino + proporcao_validacao)
    )

    if corte_treino == 0 or corte_validacao == corte_treino:
        raise ValueError("Dados insuficientes para a divisão.")

    if corte_validacao >= n:
        raise ValueError("Conjunto de teste vazio.")

    return {
        "X_treino": X.iloc[:corte_treino].copy(),
        "X_validacao": X.iloc[corte_treino:corte_validacao].copy(),
        "X_teste": X.iloc[corte_validacao:].copy(),
        "y_treino": y.iloc[:corte_treino].copy(),
        "y_validacao": y.iloc[corte_treino:corte_validacao].copy(),
        "y_teste": y.iloc[corte_validacao:].copy(),
    }

def treinar_regressao_logistica(
    X_treino: pd.DataFrame,
    y_treino: pd.Series,
):
    """
    Treina um classificador de falhas industriais.

    A padronização é ajustada exclusivamente com
    os dados de treinamento, evitando vazamento.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    if len(X_treino) != len(y_treino):
        raise ValueError("X_treino e y_treino devem ter o mesmo tamanho.")

    if y_treino.nunique() < 2:
        raise ValueError(
            "O treinamento exige exemplos das duas classes."
        )

    modelo = Pipeline(
        steps=[
            ("padronizacao", StandardScaler()),
            (
                "classificador",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    modelo.fit(X_treino, y_treino)

    return modelo

def avaliar_classificador(
    modelo,
    X_validacao: pd.DataFrame,
    y_validacao: pd.Series,
    limiar: float = 0.5,
) -> dict:
    """
    Avalia o classificador e calcula o custo
    financeiro simulado dos erros.
    """
    from sklearn.metrics import (
        accuracy_score,
        confusion_matrix,
        precision_score,
        recall_score,
    )

    from simulacao_industrial.custos_falhas import (
        calcular_custo_falhas,
    )

    if not 0 <= limiar <= 1:
        raise ValueError("O limiar deve estar entre 0 e 1.")

    if len(X_validacao) != len(y_validacao):
        raise ValueError("X e y devem ter o mesmo tamanho.")

    if len(X_validacao) == 0:
        raise ValueError("O conjunto de validação está vazio.")

    probabilidades = modelo.predict_proba(X_validacao)[:, 1]

    previsoes = (probabilidades >= limiar).astype(int)

    vn, fp, fn, vp = confusion_matrix(
        y_validacao,
        previsoes,
        labels=[0, 1],
    ).ravel()

    custo_total = calcular_custo_falhas(
        falsos_positivos=int(fp),
        falsos_negativos=int(fn),
    )

    return {
        "limiar": limiar,
        "acuracia": float(
            accuracy_score(y_validacao, previsoes)
        ),
        "precisao": float(
            precision_score(
                y_validacao,
                previsoes,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_validacao,
                previsoes,
                zero_division=0,
            )
        ),
        "verdadeiros_negativos": int(vn),
        "falsos_positivos": int(fp),
        "falsos_negativos": int(fn),
        "verdadeiros_positivos": int(vp),
        "custo_financeiro": custo_total,
    }