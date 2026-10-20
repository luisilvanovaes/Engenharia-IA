"""
Testes automatizados de clustering industrial.

Semana 04 — Dia 16
AI Energy Auditor
"""

from simulacao_industrial.gerador_dados import gerar_dados_industriais
from simulacao_industrial.clustering_industrial import executar_kmeans


def test_kmeans_tres_clusters():
    """Verifica a segmentação de 365 registros em três clusters."""

    dados = gerar_dados_industriais()

    resultado, modelo, escalador = executar_kmeans(
        dados,
        numero_clusters=3,
    )

    assert len(resultado) == 365
    assert resultado["cluster_kmeans"].nunique() == 3
    assert resultado["cluster_kmeans"].value_counts().sum() == 365

    # A função não deve modificar o DataFrame original.
    assert "cluster_kmeans" not in dados.columns

def test_kmeans_rejeita_numero_clusters_invalido():
    """Verifica se o KMeans rejeita menos de dois clusters."""
    import pytest

    dados = gerar_dados_industriais()

    with pytest.raises(
        ValueError,
        match="numero_clusters deve ser um inteiro",
    ):
        executar_kmeans(dados, numero_clusters=1)

def test_dbscan_identifica_clusters_e_ruido():
    """Verifica agrupamentos e ruído nos dados industriais."""
    from simulacao_industrial.clustering_industrial import executar_dbscan

    dados = gerar_dados_industriais()

    resultado, modelo, escalador = executar_dbscan(
        dados,
        eps=0.7,
        min_samples=5,
    )

    assert len(resultado) == 365
    assert "cluster_dbscan" in resultado.columns

    # Deve identificar três clusters e um registro como ruído.
    clusters = set(resultado["cluster_dbscan"])

    assert clusters == {-1, 0, 1, 2}
    assert (resultado["cluster_dbscan"] == -1).sum() == 1

    # O DataFrame original deve permanecer inalterado.
    assert "cluster_dbscan" not in dados.columns

def test_dbscan_rejeita_eps_invalido():
    """Verifica se o DBSCAN rejeita um eps negativo."""
    import pytest
    from simulacao_industrial.clustering_industrial import executar_dbscan

    dados = gerar_dados_industriais()

    with pytest.raises(
        ValueError,
        match="eps deve ser um número positivo e finito",
    ):
        executar_dbscan(
            dados,
            eps=-0.5,
            min_samples=5,
        )