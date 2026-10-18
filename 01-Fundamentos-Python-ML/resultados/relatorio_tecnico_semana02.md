# Relatório Técnico — Semana 02
## AI Energy Auditor | Engenharia de Inteligência Artificial

**Estado:** protótipo experimental validado tecnicamente com dados sintéticos.

### 1. Objetivo

Evoluir o projeto AI Energy Auditor por meio de processamento de dados com Pandas, avaliação de modelos de regressão, identificação estatística de anomalias e disponibilização de funcionalidades por API REST executável em Docker.

### 2. Dados e metodologia

O experimento utiliza 30 registros sintéticos de consumo energético. A variável-alvo é `consumo_kwh`, e a variável explicativa é `horas_operacao`.

A avaliação dos modelos respeitou a ordem cronológica dos dados, com sete registros de teste no período de 24 a 30 de setembro de 2026.

Foram comparadas três estratégias:

- **Baseline histórica:** média dos sete dias anteriores.
- **Regressão fixa:** treinamento único com 16 registros.
- **Regressão Walk-Forward:** treinamento com janela expansiva, iniciando com 16 registros e chegando a 22.

### 3. Resultados preditivos

| Modelo | MAE (kWh) | RMSE (kWh) |
|---|---:|---:|
| Baseline histórica | 25,4741 | 33,3481 |
| Regressão fixa | 7,6703 | 8,8188 |
| Regressão Walk-Forward | 7,4455 | 8,6282 |

A regressão Walk-Forward apresentou o menor erro, com redução relativa de 70,77% no MAE e 74,13% no RMSE em comparação à baseline.

Os percentuais representam melhoria de precisão preditiva, não redução comprovada do consumo energético.

### 4. Qualidade dos dados

Foram registradas duas auditorias de qualidade:

- `consumo_energetico_v1`: auditoria aprovada.
- `consumo_energetico_teste_defeituoso`: auditoria reprovada.

O resultado evidencia a distinção entre o dataset principal e o conjunto identificado como defeituoso. Os relatórios consolidados não detalham, isoladamente, todas as regras de qualidade responsáveis pela reprovação.

### 5. API, Docker e testes

Foi implementada uma API REST com FastAPI, incluindo endpoints de verificação de saúde, resumo e integridade dos dados, previsão de consumo e identificação de anomalias.

A aplicação foi construída e executada em Docker, com respostas HTTP 200 nos endpoints verificados.

A suíte automatizada registrou:

- **35 testes aprovados**;
- **0 falhas, 0 erros e 0 testes ignorados**;
- **1 aviso de depreciação** relacionado às dependências de teste do FastAPI.

O relatório de testes está em `resultados/relatorio_testes_semana02.xml`.

### 6. Decisões de engenharia

1. Utilizar dados sintéticos para validar o fluxo experimental antes de integrar medições reais.
2. Preservar a ordem temporal na avaliação para evitar utilização indevida de informações futuras.
3. Comparar os modelos com uma baseline histórica para contextualizar o desempenho.
4. Manter testes automatizados como evidência de regressão e funcionamento.
5. Utilizar FastAPI para disponibilizar as funcionalidades e Docker para padronizar sua execução.
6. Tratar alertas de anomalias como indicadores para investigação, não como provas de desperdício ou fraude.

### 7. Limitações e próximos passos

O dataset contém apenas 30 registros sintéticos, e a avaliação utiliza somente sete observações de teste. Os resultados não demonstram capacidade de generalização para ambientes industriais.

A disponibilidade antecipada das horas de operação é uma hipótese experimental que deverá ser verificada em produção.

Também permanecem pendentes a integração com dados operacionais reais, a avaliação em instalações industriais, o monitoramento contínuo e os controles necessários para operação em produção.

### 8. Evidências técnicas

- `notebooks/semana02_dia01_pandas.ipynb`
- `resultados/relatorio_modelos_energeticos_v1.csv`
- `resultados/metadados_experimento_energetico_v1.json`
- `resultados/relatorio_consolidado_qualidade_v1.csv`
- `resultados/resumo_executivo_qualidade_v1.json`
- `resultados/relatorio_testes_semana02.xml`
- `exercicios/api_energia.py`
- `testes/test_api_energia.py`
- `Dockerfile`
- `README.md`

**Conclusão:** a Semana 02 possui evidências de implementação e validação técnica do protótipo. A conclusão formal depende da conferência final dos artefatos e do estado do repositório.
