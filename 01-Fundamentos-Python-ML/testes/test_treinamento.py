
import sys
from pathlib import Path
import pytest

# Localizar a pasta raiz do módulo
diretorio_base = Path(__file__).resolve().parents[1]

# Permitir importar o módulo treinamento.py
sys.path.insert(0, str(diretorio_base / "exercicios"))

from treinamento import treinar_modelo


# Teste 1 — Verificar se o resultado é um dicionário
def test_resultado_e_dicionario():
    resultado = treinar_modelo(
        x=2.0,
        y_real=10.0,
        learning_rate=0.1,
        tolerancia=0.001
    )

    assert isinstance(resultado, dict)


# Teste 2 — Validar o peso final
def test_peso_final():
    resultado = treinar_modelo(
        x=2.0,
        y_real=10.0,
        learning_rate=0.1,
        tolerancia=0.001
    )

    assert resultado["peso_final"] == pytest.approx(
        4.9936, abs=1e-4
    )


# Teste 3 — Validar o número de épocas
def test_epocas_executadas():
    resultado = treinar_modelo(
        x=2.0,
        y_real=10.0,
        learning_rate=0.1,
        tolerancia=0.001
    )

    assert resultado["epocas_executadas"] == 4


# Teste 4 — Validar a perda final
def test_perda_final():
    resultado = treinar_modelo(
        x=2.0,
        y_real=10.0,
        learning_rate=0.1,
        tolerancia=0.001
    )

    assert resultado["perda_final"] < 0.001


# Teste 5 — Validar o histórico de perdas
def test_historico_perdas():
    resultado = treinar_modelo(
        x=2.0,
        y_real=10.0,
        learning_rate=0.1,
        tolerancia=0.001
    )

    assert len(resultado["historico_perdas"]) == resultado["epocas_executadas"]
