
# AI Energy Auditor

## Projeto de Engenharia de Inteligência Artificial

### 1. Objetivo

Desenvolver progressivamente um sistema de auditoria
energética utilizando Python, análise de dados,
estatística, Machine Learning e práticas de Engenharia
de Inteligência Artificial.

### 2. Ambiente de desenvolvimento

- Sistema operacional: Windows 11
- Python: 3.12.10
- Ambiente virtual: .venv
- Editor: Visual Studio Code
- Ambiente interativo: Jupyter
- Testes automatizados: pytest

### 3. Estrutura do projeto

- aulas/: experimentos introdutórios
- dados/: datasets utilizados
- datasets/: diretório reservado para conjuntos de dados
- exercicios/: implementações em Python
- notebooks/: experimentos documentados
- testes/: testes automatizados
- resultados/: métricas e relatórios
- checkpoints/: registros de acompanhamento

### 4. Experimento de consumo energético

O primeiro experimento utiliza um conjunto sintético
de 30 registros diários de consumo energético.

Variáveis:

- data
- horas_operacao
- consumo_kwh

### 5. Metodologia de avaliação

Foi utilizada validação temporal walk-forward
com janela de treinamento expansiva.

Modelos comparados:

- Baseline temporal baseado na média histórica
- Regressão linear por mínimos quadrados

### 6. Resultados experimentais

Baseline temporal:

- MAE: 33.6644 kWh
- RMSE: 38.3879 kWh

Regressão linear:

- MAE: 9.8871 kWh
- RMSE: 10.7783 kWh

Redução do MAE: 70.63%

A redução representa melhoria na precisão das
previsões, não economia real de energia.

### 7. Reprodutibilidade

O experimento utiliza geração determinística
de dados sintéticos, com seed 2026.

O manifesto de reprodutibilidade está disponível em:

resultados/exercicio34_manifesto.json

### 8. Testes automatizados

Foram implementados 16 testes automatizados
utilizando pytest.

Resultado da última execução validada:

- 16 testes aprovados
- 0 falhas
- 0 erros
- 0 testes ignorados

Relatório:

resultados/exercicio35_testes.xml

### 9. Estado atual

Protótipo experimental em desenvolvimento.

Os resultados foram obtidos com dados sintéticos
e não constituem uma auditoria energética real.

### 10. Documentação técnica

Os conceitos, implementações, testes, resultados
e lições aprendidas serão consolidados em um
livro técnico de Engenharia de Inteligência Artificial.
