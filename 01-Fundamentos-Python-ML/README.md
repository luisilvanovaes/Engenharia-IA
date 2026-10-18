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
