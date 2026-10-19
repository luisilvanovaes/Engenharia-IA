"""Cálculo dos custos de erros na detecção de falhas industriais."""


def calcular_custo_falhas(
    falsos_positivos: int,
    falsos_negativos: int,
    custo_falso_positivo: float = 150.0,
    custo_falso_negativo: float = 2000.0,
) -> float:
    """
    Calcula o custo financeiro dos erros de classificação.

    Os custos padrão são hipóteses simuladas para o
    projeto AI Energy Auditor, expressas em reais (BRL).
    """

    if falsos_positivos < 0 or falsos_negativos < 0:
        raise ValueError(
            "A quantidade de erros não pode ser negativa."
        )

    if custo_falso_positivo < 0 or custo_falso_negativo < 0:
        raise ValueError(
            "Os custos financeiros não podem ser negativos."
        )

    custo_total = (
        falsos_positivos * custo_falso_positivo
        + falsos_negativos * custo_falso_negativo
    )

    return float(custo_total)