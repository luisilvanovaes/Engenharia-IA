from fastapi.testclient import TestClient
from exercicios.api_energia import app

cliente = TestClient(app)


def test_health():
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_resumo_energetico():
    resposta = cliente.get("/dados/resumo")
    assert resposta.status_code == 200
    assert resposta.json()["total_registros"] == 30
    assert resposta.json()["consumo_total_kwh"] == 6504.224


def test_integridade():
    resposta = cliente.get("/dados/integridade")
    assert resposta.status_code == 200
    resultado = resposta.json()
    assert resultado["algoritmo"] == "SHA-256"
    assert resultado["sha256"] == (
        "c24a08ea24623e98ac6b180e0ce9aa0b74e9807a3433882906f42e93884144de"
    )


def test_previsao_ridge():
    resposta = cliente.post(
        "/previsao",
        json={"horas_operacao": 8.0}
    )
    assert resposta.status_code == 200
    assert resposta.json()["consumo_previsto_kwh"] == 194.8141


def test_previsao_invalida():
    for horas in [-1, 0, 25]:
        resposta = cliente.post(
            "/previsao",
            json={"horas_operacao": horas}
        )
        assert resposta.status_code == 422


def test_anomalias():
    resposta = cliente.get("/anomalias")
    assert resposta.status_code == 200

    resultado = resposta.json()
    assert resultado["total_registros_analisados"] == 30
    assert resultado["total_registros_sinalizados"] == 6

    esperados = {
        "2026-09-17": {"Isolation Forest", "LOF"},
        "2026-09-29": {"Isolation Forest", "IQR"},
        "2026-09-06": {"LOF"},
        "2026-09-16": {"Isolation Forest"},
        "2026-09-19": {"IQR"},
        "2026-09-30": {"LOF"},
    }

    alertas = resultado["alertas"]
    assert {a["data"] for a in alertas} == set(esperados)

    for alerta in alertas:
        assert set(alerta["metodos"]) == esperados[alerta["data"]]
        assert alerta["total_alertas"] == len(alerta["metodos"])
        assert alerta["prioridade"] == (
            "Alta - investigar"
            if alerta["total_alertas"] >= 2
            else "Revisao - verificar"
        )


def test_rota_inexistente():
    resposta = cliente.get("/rota-inexistente")
    assert resposta.status_code == 404
