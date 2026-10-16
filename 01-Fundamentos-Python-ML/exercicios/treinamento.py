
def treinar_modelo(
    x,
    y_real,
    peso_inicial=1.0,
    learning_rate=0.1,
    max_epocas=100,
    tolerancia=0.001
):
    # 1. Inicializar as variáveis
    w = peso_inicial
    historico_perdas = []

    # 2. Executar o treinamento
    for epoca in range(max_epocas):

        # Calcular previsão e perda
        y_previsto = w * x
        perda = (y_previsto - y_real) ** 2

        # Calcular o gradiente
        gradiente = 2 * x * (y_previsto - y_real)

        # Atualizar o peso
        w = w - learning_rate * gradiente

        # Calcular a perda após a atualização
        previsao_atualizada = w * x
        perda_atualizada = (previsao_atualizada - y_real) ** 2

        # Registrar o histórico
        historico_perdas.append(perda_atualizada)

        # Aplicar Early Stopping
        if perda_atualizada < tolerancia:
            break

    # 3. Calcular os resultados finais
    previsao_final = w * x
    perda_final = (previsao_final - y_real) ** 2

    # 4. Retornar os resultados
    return {
        "peso_final": w,
        "previsao_final": previsao_final,
        "perda_final": perda_final,
        "epocas_executadas": len(historico_perdas),
        "historico_perdas": historico_perdas
    }
