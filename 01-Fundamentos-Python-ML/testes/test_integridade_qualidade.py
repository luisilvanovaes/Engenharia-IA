
# ============================================================
# SEMANA 02 — EXERCÍCIO 61 — ETAPA 2
# Testes da implementação compartilhada de SHA-256
# ============================================================

import hashlib

import pytest

from exercicios.integridade_qualidade import (
    calcular_sha256_artefato
)


def test_sha256_arquivo_conhecido(tmp_path):

    arquivo = tmp_path / "teste.txt"
    arquivo.write_bytes(b"abc")

    resultado = calcular_sha256_artefato(arquivo)

    esperado = hashlib.sha256(b"abc").hexdigest()

    assert resultado == esperado
    assert len(resultado) == 64


def test_sha256_detecta_alteracao(tmp_path):

    arquivo = tmp_path / "teste.txt"

    arquivo.write_bytes(b"conteudo original")
    hash_original = calcular_sha256_artefato(arquivo)

    arquivo.write_bytes(b"conteudo alterado")
    hash_alterado = calcular_sha256_artefato(arquivo)

    assert hash_original != hash_alterado


def test_sha256_arquivo_ausente(tmp_path):

    arquivo = tmp_path / "inexistente.txt"

    with pytest.raises(FileNotFoundError):
        calcular_sha256_artefato(arquivo)


def test_sha256_arquivo_vazio(tmp_path):

    arquivo = tmp_path / "vazio.txt"
    arquivo.write_bytes(b"")

    resultado = calcular_sha256_artefato(arquivo)

    esperado = hashlib.sha256(b"").hexdigest()

    assert resultado == esperado



# ============================================================
# SEMANA 02 — EXERCÍCIO 62 — ETAPA 1
# Teste de leitura de arquivos em múltiplos blocos
# ============================================================

def test_sha256_arquivo_multiplos_blocos(tmp_path):
    """
    Verifica o cálculo SHA-256 de um arquivo maior
    que o bloco de leitura de 65.536 bytes.
    """

    arquivo = tmp_path / "arquivo_grande.bin"

    # 200.000 bytes: exige múltiplas leituras.
    conteudo = b"AI_ENERGY_AUDITOR_" * 10000

    assert len(conteudo) > 65536

    arquivo.write_bytes(conteudo)

    # Hash calculado pela implementação do projeto.
    resultado = calcular_sha256_artefato(arquivo)

    # Hash de referência calculado diretamente na memória.
    esperado = hashlib.sha256(conteudo).hexdigest()

    assert resultado == esperado
    assert len(resultado) == 64

    print(
        f"\nArquivo validado: {len(conteudo)} bytes"
    )



# ============================================================
# SEMANA 02 — EXERCÍCIO 62 — ETAPA 2
# Testes de arquivos binários e alterações mínimas
# ============================================================


def test_sha256_arquivo_binario(tmp_path):
    """
    Verifica se a função calcula corretamente
    o SHA-256 de dados binários.
    """

    arquivo = tmp_path / "dados.bin"

    conteudo = bytes(range(256))

    arquivo.write_bytes(conteudo)

    resultado = calcular_sha256_artefato(arquivo)

    esperado = hashlib.sha256(conteudo).hexdigest()

    assert resultado == esperado
    assert len(resultado) == 64


def test_sha256_detecta_alteracao_de_um_byte(tmp_path):
    """
    Verifica se a alteração de apenas um byte
    produz um SHA-256 diferente.
    """

    arquivo = tmp_path / "auditoria.bin"

    conteudo_original = bytearray(
        b"AI_ENERGY_AUDITOR_2026"
    )

    arquivo.write_bytes(conteudo_original)

    hash_original = calcular_sha256_artefato(arquivo)

    # Alterar somente o primeiro byte.
    conteudo_alterado = conteudo_original.copy()

    conteudo_alterado[0] ^= 1

    arquivo.write_bytes(conteudo_alterado)

    hash_alterado = calcular_sha256_artefato(arquivo)

    assert len(conteudo_original) == len(conteudo_alterado)

    assert sum(
        a != b
        for a, b in zip(
            conteudo_original,
            conteudo_alterado
        )
    ) == 1

    assert hash_original != hash_alterado


# ============================================================
# SEMANA 02 — EXERCÍCIO 62 — ETAPA 3
# Testes dos limites de leitura em blocos
# ============================================================


@pytest.mark.parametrize(
    "tamanho",
    [
        65535,   # Um byte abaixo do limite
        65536,   # Exatamente um bloco
        65537,   # Um byte acima do limite
        131072,  # Exatamente dois blocos
        131073   # Dois blocos mais um byte
    ]
)
def test_sha256_limites_de_blocos(tmp_path, tamanho):
    """
    Verifica se o SHA-256 é calculado corretamente
    em diferentes limites de leitura.
    """

    arquivo = tmp_path / f"arquivo_{tamanho}.bin"

    # Gerar conteúdo determinístico com o tamanho desejado.
    conteudo = bytes(
        indice % 256
        for indice in range(tamanho)
    )

    arquivo.write_bytes(conteudo)

    # Calcular com a implementação do projeto.
    resultado = calcular_sha256_artefato(arquivo)

    # Calcular referência diretamente na memória.
    esperado = hashlib.sha256(conteudo).hexdigest()

    assert arquivo.stat().st_size == tamanho
    assert resultado == esperado
    assert len(resultado) == 64
