
# ============================================================
# AI ENERGY AUDITOR
# Módulo reutilizável de integridade criptográfica
# ============================================================

import hashlib
from pathlib import Path


def calcular_sha256_artefato(caminho_arquivo):
    """
    Calcula o SHA-256 de um arquivo.

    Utiliza leitura em blocos para evitar carregar
    o arquivo inteiro na memória.
    """

    caminho = Path(caminho_arquivo)

    if not caminho.is_file():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        )

    sha256 = hashlib.sha256()

    with caminho.open("rb") as arquivo:
        for bloco in iter(
            lambda: arquivo.read(65536),
            b""
        ):
            sha256.update(bloco)

    return sha256.hexdigest()
