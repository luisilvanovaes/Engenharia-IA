# AI Energy Auditor

**Projeto aplicado de Engenharia de Inteligência Artificial — Semana 01**

> **Estado:** protótipo experimental com dados sintéticos. A validação técnica da Semana 01 foi realizada; o sistema ainda não constitui uma auditoria energética operacional.

## 1. Objetivo e escopo

Desenvolver progressivamente um sistema de apoio à auditoria energética por meio de Python, computação numérica, estatística, aprendizado de máquina e práticas de Engenharia de Inteligência Artificial.

Na Semana 01, o projeto consolida fundamentos matemáticos e computacionais e os aplica a um experimento de previsão de consumo elétrico. A redução do erro de previsão **não representa economia efetiva de energia** nem demonstra, isoladamente, a existência de desperdícios ou fraudes.

## 2. Ambiente de desenvolvimento

O ambiente utilizado nas validações foi:

| Componente | Configuração |
|---|---|
| Sistema operacional | Windows 11 |
| Python | 3.12.10 |
| Ambiente virtual | `.venv` |
| Editor | Visual Studio Code |
| Ambiente interativo | Jupyter / JupyterLab |
| Testes automatizados | `pytest` |

As versões das bibliotecas do experimento foram registradas no manifesto de reprodutibilidade em `resultados/exercicio34_manifesto.json`.

Os comandos apresentados neste documento pressupõem um terminal PowerShell aberto na raiz do projeto, com o ambiente virtual ativado.

## 3. Organização do projeto

| Diretório ou arquivo | Finalidade |
|---|---|
| `aulas/` | Experimentos introdutórios |
| `dados/` | Dados utilizados pelo projeto |
| `datasets/` | Diretório reservado para conjuntos de dados |
| `exercicios/` | Implementações em Python |
| `notebooks/` | Experimentos e explicações em Jupyter |
| `testes/` | Testes automatizados |
| `resultados/` | Relatórios, métricas e evidências de execução |
| `checkpoints/` | Registros de acompanhamento e validação |
| `backups/` | Cópias de segurança do trabalho |
| `README.md` | Visão geral e instruções de reprodução |

O notebook principal é `notebooks/semana01_dia01_numpy.ipynb`. Após a organização documental e a remoção de uma célula vazia, foram registradas **116 células: 80 de código e 36 Markdown**.

## 4. Fundamentos desenvolvidos

O notebook reúne atividades sobre:

- Arrays NumPy, operações vetorizadas e *broadcasting*;
- Álgebra linear, operações matriciais, normas e projeções;
- Fundamentos de redes neurais, funções de ativação e funções de perda;
- Descida do gradiente (*Gradient Descent*), taxas de aprendizado, parada antecipada (*Early Stopping*) e checkpoints;
- Funções reutilizáveis e testes automatizados;
- Estatística descritiva e regressão linear;
- Validação temporal *walk-forward* e reprodutibilidade experimental.

Os exercícios do notebook são atividades didáticas progressivas. Sua numeração local não deve ser interpretada como a numeração oficial de dias do plano de treinamento.

## 5. Experimento de consumo energético

O experimento utiliza **30 registros diários sintéticos** com as variáveis:

| Variável | Significado |
|---|---|
| `data` | Data da observação |
| `horas_operacao` | Horas de operação representadas no registro |
| `consumo_kwh` | Consumo energético diário, em kWh |

O conjunto de dados é gerado deterministicamente com semente aleatória **2026**. A formulação experimental inclui uma parcela fixa de consumo, uma parcela proporcional às horas de operação e ruído aleatório.

Arquivo de dados: `dados/consumo_energetico_v1.csv`.

**Limitação:** dados simulados são úteis para verificar algoritmos e processos, mas não substituem medições reais, contextualização operacional nem validação em campo.

## 6. Metodologia de avaliação

Foi utilizada validação temporal **walk-forward com janela de treinamento expansiva**. A avaliação começou com 15 observações de treinamento e produziu **15 previsões** para os registros seguintes, respeitando a ordem temporal.

Foram comparados dois métodos:

1. **Baseline temporal:** previsão baseada na média histórica disponível até cada instante.
2. **Regressão linear:** modelo ajustado por mínimos quadrados com base nas observações de treinamento disponíveis.

As métricas são:

- **MAE (*Mean Absolute Error*):** média dos valores absolutos dos erros de previsão.
- **RMSE (*Root Mean Squared Error*):** raiz quadrada da média dos erros ao quadrado, mais sensível a erros elevados.

Ambas são expressas em **kWh** neste experimento; valores menores indicam previsões mais próximas dos dados observados.

## 7. Resultados experimentais

| Modelo | MAE (kWh) | RMSE (kWh) |
|---|---:|---:|
| Baseline temporal | 33,6644 | 38,3879 |
| Regressão linear | 9,8871 | 10,7783 |

A regressão linear apresentou uma **redução relativa de 70,63% no MAE** em comparação ao baseline temporal, no conjunto sintético avaliado.

Essa melhoria é exclusivamente de **precisão preditiva**. Não é uma redução de consumo elétrico, de custos ou de desperdício energético. O resultado também não permite generalizar o desempenho para instalações reais sem novas avaliações.

Relatório de referência: `resultados/exercicio33_relatorio.json`.

## 8. Reprodutibilidade e integridade

A reprodução do experimento depende da preservação dos dados, dos parâmetros de geração e do ambiente de execução.

Artefatos registrados:

- `dados/consumo_energetico_v1.csv` — conjunto de dados sintético;
- `resultados/exercicio34_manifesto.json` — parâmetros, versões e hash do dataset;
- `resultados/exercicio36_integridade.json` — registro de conferência de integridade;
- `checkpoints/checkpoint_semana01.json` — acompanhamento da consolidação técnica.

O SHA-256 registrado para o dataset original é:

```text
c24a08ea24623e98ac6b180e0ce9aa0b74e9807a3433882906f42e93884144de
```

Para verificar o arquivo atual no PowerShell:

```powershell
(Get-FileHash .\dados\consumo_energetico_v1.csv -Algorithm SHA256).Hash
```

O valor obtido deve coincidir com o hash registrado, desde que o dataset não tenha sido modificado.

## 9. Testes automatizados e execução do notebook

Os testes existentes verificam a integridade do dataset e propriedades da função de treinamento.

Na última execução informada, foram aprovados **16 testes**, sem falhas, erros ou testes ignorados:

- 11 testes de integridade dos dados;
- 5 testes de treinamento.

Para executar novamente:

```powershell
python -m pytest testes/ -v
```

O relatório XML registrado anteriormente está em `resultados/exercicio35_testes.xml`. Esse arquivo representa uma execução registrada e não é atualizado automaticamente pelo comando acima.

O notebook também foi executado sequencialmente em um novo kernel com:

```powershell
python -m jupyter nbconvert --to notebook --execute "notebooks/semana01_dia01_numpy.ipynb" --output "semana01_validacao_execucao.ipynb" --output-dir "resultados" --ExecutePreprocessor.timeout=300
```

Na execução de validação, as **80 células com código não vazio** foram executadas sem erros. O arquivo de saída dessa validação foi `resultados/semana01_validacao_execucao.ipynb`. Posteriormente, a célula vazia foi removida do notebook principal; a alteração foi apenas estrutural.

Os testes automatizados e a execução do notebook são evidências complementares. Nenhum deles, isoladamente, comprova que o protótipo está pronto para uso em produção.

## 10. Estado atual, limitações e documentação futura

**Estado atual:** consolidação técnica da Semana 01. O notebook está documentado, a execução das células com código foi validada e os testes automatizados passaram. O checkpoint do projeto registra o estado `consolidacao_final`.

**Limitações principais:**

- O conjunto de dados é sintético e pequeno (30 observações).
- O experimento mede qualidade de previsão, não economia de energia.
- Ainda não há integração comprovada com medidores, sensores, sistemas industriais ou dados operacionais reais.
- Não há demonstração de detecção de desperdícios ou fraudes em ambiente real.
- A validação em produção, a governança de dados e os aspectos operacionais permanecem como trabalho futuro.

**Documentação para o livro técnico:** os conceitos, implementações, testes, resultados, dificuldades e lições aprendidas da formação serão consolidados em capítulos de Engenharia de Inteligência Artificial. O notebook e os artefatos citados neste README são fontes técnicas desse registro.

A revisão integral deste README constitui uma etapa documental; a marcação de conclusão no checkpoint deve ocorrer **somente após a versão revisada ser incorporada e conferida no projeto local**.

---

## 11. Semana 02 — Pandas, Machine Learning e API

### 11.1. Evolução do projeto

Na Semana 02, o AI Energy Auditor evoluiu do experimento inicial para um protótipo com processamento de dados, avaliação de modelos preditivos, identificação estatística de anomalias e disponibilização de funcionalidades por uma API REST.

O notebook de referência é `notebooks/semana02_dia01_pandas.ipynb`.

As atividades abordaram:

- Manipulação e análise de dados com Pandas;
- Verificações de qualidade e integridade dos dados;
- Engenharia de atributos temporais;
- Avaliação cronológica de modelos de regressão;
- Comparação com baseline histórica;
- Identificação estatística de observações anômalas;
- Desenvolvimento de API com FastAPI;
- Testes automatizados com Pytest;
- Empacotamento e execução com Docker.

### 11.2. Avaliação dos modelos energéticos

Foram avaliados três métodos sobre sete registros de teste, correspondentes ao período de 24 a 30 de setembro de 2026.

| Modelo | MAE (kWh) | RMSE (kWh) |
|---|---:|---:|
| Regressão Walk-Forward | 7,4455 | 8,6282 |
| Regressão fixa | 7,6703 | 8,8188 |
| Baseline histórica | 25,4741 | 33,3481 |

A regressão Walk-Forward apresentou redução relativa de 70,77% no MAE e de 74,13% no RMSE em comparação à baseline histórica.

Fonte: `resultados/relatorio_modelos_energeticos_v1.csv`.

Esses percentuais representam melhoria de precisão preditiva, não redução comprovada do consumo de energia.

### 11.3. API REST

A API está implementada em `exercicios/api_energia.py` utilizando FastAPI.

Endpoints validados:

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/health` | Verificação de funcionamento |
| GET | `/dados/resumo` | Resumo do conjunto de dados |
| GET | `/dados/integridade` | Verificação de integridade |
| POST | `/previsao` | Previsão de consumo energético |
| GET | `/anomalias` | Identificação de observações anômalas |
| GET | `/docs` | Documentação interativa da API |
| GET | `/openapi.json` | Especificação OpenAPI |

Exemplo de entrada para `POST /previsao`:

```json
{"horas_operacao": 8}
```

A identificação de anomalias é um mecanismo de triagem estatística. Seus resultados não comprovam, isoladamente, desperdícios, irregularidades ou fraudes.

### 11.4. Execução com Docker

A imagem da aplicação pode ser construída na raiz deste módulo:

```powershell
docker build -t ai-energy-auditor:v1 -f Dockerfile .
```

Para iniciar um contêiner:

```powershell
docker run -d --name ai-energy-auditor-api -p 8000:8000 ai-energy-auditor:v1
```

Com o contêiner em execução, a documentação interativa fica disponível em:

`http://localhost:8000/docs`

O comando de inicialização pressupõe que não exista outro contêiner com o mesmo nome e que a porta 8000 esteja disponível.

### 11.5. Testes automatizados

A suíte de testes foi executada com:

```powershell
python -m pytest testes/ -q --junitxml=resultados/relatorio_testes_semana02.xml
```

Resultado validado:

- 35 testes executados e aprovados;
- Zero falhas;
- Zero erros;
- Zero testes ignorados;
- Um aviso de depreciação relacionado às dependências de teste do FastAPI.

O relatório atualizado está em `resultados/relatorio_testes_semana02.xml`.

### 11.6. Limitações e decisões de engenharia

- O conjunto de dados permanece sintético, com 30 registros.
- A avaliação preditiva utiliza uma amostra de teste pequena.
- A validação temporal procura preservar a ordem cronológica dos dados.
- A baseline histórica fornece uma referência para interpretar o desempenho dos modelos.
- As previsões e anomalias não constituem comprovação de economia energética ou fraude.
- A API e o Docker demonstram capacidade de execução técnica, não prontidão para produção.
- Permanecem pendentes a validação com dados reais, o monitoramento operacional e a avaliação em instalações industriais.

O relatório técnico semanal deve consolidar as métricas, limitações, decisões de engenharia e evidências de validação antes do encerramento formal da Semana 02.


## 12. Semana 03 — Machine Learning supervisionado avançado

### 12.1. Formulação do problema — Exercício 61

O AI Energy Auditor passou a contemplar dois problemas distintos:

- **Previsão energética:** estimar o consumo futuro de energia, em kWh, utilizando informações disponíveis antes do período previsto.
- **Detecção de falhas operacionais:** classificar retrospectivamente períodos de operação como normais ou com falha, utilizando medições já observadas.

Esses problemas não devem ser confundidos. O classificador implementado nesta etapa não prevê falhas antes de sua ocorrência.

### 12.2. Simulação industrial — Exercícios 62 e 63

Foi implementado um gerador de dados industriais sintéticos em `simulacao_industrial/gerador_dados.py`.

O simulador produz 365 registros diários, com semente aleatória fixa, incluindo:

- Turnos planejados;
- Horas de operação;
- Produção industrial;
- Temperatura ambiente;
- Consumo energético em kWh;
- Indicador binário de falha operacional;
- Consumo do dia anterior;
- Média histórica de consumo dos sete dias anteriores.

As falhas simuladas acrescentam consumo energético ao processo industrial.

Na execução utilizada para o exercício, foram geradas 33 falhas em 365 dias. Após a remoção dos registros sem histórico completo, permaneceram 358 observações, das quais 32 continham falhas.

### 12.3. Modelo de Regressão Logística — Exercício 64

Arquivo: `simulacao_industrial/classificador_falhas.py`.

O classificador foi implementado com Scikit-learn, utilizando:

- `StandardScaler` para padronização;
- `LogisticRegression` para classificação binária;
- `class_weight="balanced"` para tratamento inicial do desbalanceamento;
- `max_iter=1000`;
- `random_state=42`.

A padronização é ajustada exclusivamente com os dados de treinamento, por meio de um pipeline.

Os dados são divididos cronologicamente, sem embaralhamento:

| Conjunto | Registros | Falhas |
|---|---:|---:|
| Treinamento | 250 | 24 |
| Validação | 54 | 4 |
| Teste | 54 | 4 |
| **Total** | **358** | **32** |

O conjunto de teste permanece reservado para avaliação posterior.

### 12.4. Resultados da validação

Com limiar de classificação de 0,50, foram obtidos os seguintes resultados:

| Indicador | Resultado |
|---|---:|
| Acurácia | 100% |
| Precisão | 100% |
| Recall | 100% |
| Verdadeiros negativos | 50 |
| Verdadeiros positivos | 4 |
| Falsos positivos | 0 |
| Falsos negativos | 0 |
| Brier Score | 0,015902 |
| Log Loss | 0,121535 |

As probabilidades médias estimadas foram de 81,62% nos dias com falha e 10,66% nos dias normais.

Esses resultados são específicos do conjunto sintético de validação e não demonstram desempenho equivalente em instalações industriais reais.

### 12.5. Custos financeiros simulados

Arquivo: `simulacao_industrial/custos_falhas.py`.

Foi definida uma função de custo para erros de classificação:

**Custo total = R$ 150 × falsos positivos + R$ 2.000 × falsos negativos.**

Os valores são hipóteses financeiras utilizadas para fins didáticos e de comparação entre modelos.

Na validação realizada, o custo calculado dos erros foi de **R$ 0,00**, pois não ocorreram falsos positivos nem falsos negativos.

Esse resultado não representa economia energética comprovada, ausência de custos operacionais ou retorno financeiro real.

### 12.6. Interpretação dos coeficientes

Os coeficientes do modelo, após padronização das variáveis, foram:

| Variável | Coeficiente |
|---|---:|
| `consumo_kwh` | +6,3380 |
| `producao_unidades` | -2,3302 |
| `horas_operacao` | -2,1191 |
| `turnos_planejados` | -1,5973 |
| `temperatura_ambiente_c` | -0,8812 |
| `consumo_kwh_dia_anterior` | -0,2157 |
| `media_consumo_7d` | +0,1065 |

O consumo energético apresentou o maior coeficiente positivo.

Esse comportamento é compatível com o mecanismo do simulador, no qual falhas aumentam o consumo. Os coeficientes não devem ser interpretados como evidência de causalidade.

### 12.7. Testes e integração contínua

Foi criado o arquivo `testes/test_classificador_falhas.py`, com testes de treinamento, avaliação e rejeição de limiar inválido.

A suíte completa apresentou:

- **56 testes aprovados**;
- Zero falhas;
- Um aviso de depreciação relacionado à integração de testes do FastAPI.

O commit `4ce2122` foi enviado à branch `main`.

O workflow **Testes Python #11**, no GitHub Actions, foi concluído com sucesso.

### 12.8. Limitações e próximas melhorias

As principais limitações identificadas são:

1. Os dados são integralmente simulados.
2. Existem apenas quatro falhas no conjunto de validação, tornando as métricas pouco robustas.
3. O mecanismo de geração das falhas pode facilitar artificialmente sua identificação.
4. O classificador utiliza o consumo observado no próprio dia e, portanto, realiza detecção retrospectiva, não previsão antecipada.
5. A calibração das probabilidades ainda exige avaliação mais abrangente.
6. Os custos financeiros são hipotéticos e precisam ser validados com dados operacionais reais.
7. Ainda não foram realizados testes industriais de campo.

**Próximas etapas:** comparar árvores de decisão e ensembles, estudar estabilidade e sobreajuste, implementar validação e ajuste de hiperparâmetros, avaliar modelos por métricas e custos e reservar o conjunto de teste para a avaliação final.

O objetivo permanece desenvolver progressivamente um sistema de apoio à auditoria energética industrial, com rastreabilidade, reprodutibilidade e validação técnica.

### 12.9. Exercício 65 — Árvores de decisão e ensembles

**Objetivo:** comparar três classificadores para detecção retrospectiva de falhas industriais, analisando desempenho, custo financeiro simulado, importância das variáveis, sobreajuste e estabilidade.

#### 12.9.1. Modelos implementados

Arquivo: `simulacao_industrial/comparador_modelos.py`.

Foram implementados três estimadores:

1. **Regressão Logística:** padronização das variáveis e ponderação das classes.
2. **Árvore de Decisão:** profundidade máxima de 4 e mínimo de 5 amostras por folha.
3. **Random Forest:** 100 árvores, profundidade máxima de 6 e mínimo de 3 amostras por folha.

Todos foram treinados com os mesmos dados e avaliados utilizando uma divisão temporal, sem embaralhamento.

O conjunto de teste permaneceu reservado para avaliação futura.

#### 12.9.2. Comparação dos resultados

A validação utilizou 54 registros, incluindo quatro falhas operacionais.

| Métrica | Regressão Logística | Árvore de Decisão | Random Forest |
|---|---:|---:|---:|
| Acurácia | 100% | 74,07% | 88,89% |
| Precisão | 100% | 18,75% | 33,33% |
| Recall | 100% | 75% | 50% |
| Falsos positivos | 0 | 13 | 4 |
| Falsos negativos | 0 | 1 | 2 |
| Custo financeiro simulado | R$ 0 | R$ 3.950 | R$ 4.600 |

A Regressão Logística apresentou o melhor desempenho nesta validação.

Entretanto, os resultados não demonstram superioridade universal do modelo, pois os dados são sintéticos e existem apenas quatro falhas no conjunto de validação.

A função de custo utilizada foi:

**Custo total = R$ 150 × falsos positivos + R$ 2.000 × falsos negativos.**

Esses valores representam hipóteses financeiras didáticas, não prejuízos ou economias reais.

#### 12.9.3. Importância das variáveis

A Random Forest apresentou as seguintes importâncias:

| Variável | Importância |
|---|---:|
| `consumo_kwh` | 0,3863 |
| `consumo_kwh_dia_anterior` | 0,1435 |
| `producao_unidades` | 0,1228 |
| `horas_operacao` | 0,1179 |
| `media_consumo_7d` | 0,1072 |
| `temperatura_ambiente_c` | 0,1008 |
| `turnos_planejados` | 0,0216 |

O consumo energético diário apresentou a maior importância.

Esse resultado é compatível com o mecanismo de simulação, no qual as falhas aumentam artificialmente o consumo.

As importâncias são calculadas a partir da redução de impureza das árvores. Não demonstram causalidade e podem ser influenciadas pela correlação entre variáveis.

#### 12.9.4. Análise de possível sobreajuste

Foram comparados os valores de recall nos conjuntos de treinamento e validação.

| Modelo | Recall no treinamento | Recall na validação |
|---|---:|---:|
| Regressão Logística | 100% | 100% |
| Árvore de Decisão | 91,67% | 75% |
| Random Forest | 100% | 50% |

A Random Forest apresentou a maior diferença entre treinamento e validação, sugerindo possível dificuldade de generalização.

Essa diferença, isoladamente, não comprova sobreajuste, especialmente diante do pequeno número de falhas na validação.

#### 12.9.5. Análise de estabilidade

A Random Forest foi treinada novamente com cinco sementes aleatórias, mantendo os dados e os demais hiperparâmetros constantes.

| Semente | Recall | Custo financeiro simulado |
|---|---:|---:|
| 10 | 75% | R$ 2.600 |
| 21 | 75% | R$ 2.750 |
| 42 | 50% | R$ 4.600 |
| 84 | 75% | R$ 2.600 |
| 123 | 50% | R$ 4.750 |

O custo médio foi de **R$ 3.460**, com amplitude de **R$ 2.150**.

A variação dos resultados indica sensibilidade à semente aleatória nesta configuração experimental.

Não é possível generalizar essa conclusão para outros conjuntos de dados sem avaliações adicionais.

#### 12.9.6. Testes automatizados e integração contínua

Foi criado o arquivo `testes/test_comparador_modelos.py`, contendo quatro testes:

1. Treinamento dos três estimadores.
2. Rejeição de conjuntos vazios.
3. Rejeição de conjuntos com tamanhos incompatíveis.
4. Rejeição de treinamento contendo apenas uma classe.

A suíte completa apresentou:

- **60 testes aprovados**;
- Zero falhas;
- Um aviso de depreciação relacionado à integração Starlette/HTTPX.

O commit `e0b911c` foi enviado à branch `main`.

O workflow **Testes Python #13**, no GitHub Actions, foi concluído com sucesso.

#### 12.9.7. Limitações e decisões de engenharia

As principais limitações identificadas são:

1. Os dados utilizados são integralmente simulados.
2. Existem apenas quatro falhas na validação.
3. O mecanismo de geração das falhas pode favorecer artificialmente determinados modelos.
4. O uso do consumo observado no próprio dia caracteriza detecção retrospectiva, não previsão antecipada de falhas.
5. A importância das variáveis não deve ser interpretada como causalidade.
6. Os custos financeiros são hipotéticos.
7. A estabilidade foi investigada apenas para a Random Forest, com cinco sementes e uma única divisão temporal.
8. O conjunto de teste ainda não foi utilizado.

**Decisão provisória:** manter a Regressão Logística como referência de comparação, sem declarar um modelo definitivo para implantação industrial.

**Próxima etapa — Dia 14:** estudar validação temporal, vazamento de dados e ajuste de hiperparâmetros com `RandomizedSearchCV`, preservando a separação entre treinamento, validação e teste.

O objetivo continua sendo desenvolver o AI Energy Auditor com critérios técnicos de reprodutibilidade, rastreabilidade e avaliação de custos operacionais.
