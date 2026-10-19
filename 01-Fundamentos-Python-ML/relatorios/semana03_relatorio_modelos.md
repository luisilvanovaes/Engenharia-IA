# AI Energy Auditor — Relatório Técnico da Semana 03

**Curso:** Engenharia de Inteligência Artificial  
**Módulo:** Machine Learning Supervisionado Avançado  
**Semana:** 03 — Exercícios 61 a 67  
**Projeto:** AI Energy Auditor  
**Data do registro:** 19/10/2026  
**Status:** Comparador implementado, testes locais aprovados e integração contínua validada.

---

## 1. Resumo executivo

Durante a Semana 03, foi desenvolvido um sistema experimental de classificação de falhas operacionais industriais, utilizando dados sintéticos de consumo energético, produção, temperatura e operação.

Foram implementados e comparados quatro classificadores:

1. Regressão Logística;
2. Árvore de Decisão;
3. Random Forest;
4. Random Forest com ajuste de hiperparâmetros.

A avaliação considerou acurácia, precisão, recall, falsos positivos, falsos negativos e custos financeiros simulados.

**Resultado principal:** a Regressão Logística apresentou o menor custo de classificação no conjunto de validação utilizado.

Essa conclusão é provisória e não representa comprovação de desempenho em ambiente industrial real.

## 2. Objetivo do problema

Identificar retrospectivamente dias com falhas operacionais, utilizando informações observadas no próprio dia.

**Variável-alvo:** `falha_operacional`

- `0`: operação normal;
- `1`: ocorrência de falha operacional simulada.

### 2.1. Variáveis de entrada

- `turnos_planejados`
- `horas_operacao`
- `producao_unidades`
- `temperatura_ambiente_c`
- `consumo_kwh`
- `consumo_kwh_dia_anterior`
- `media_consumo_7d`

A variável-alvo não é utilizada como entrada do classificador.

**Limitação importante:** como o modelo utiliza o consumo energético e outras informações do próprio dia, trata-se de detecção retrospectiva, e não de previsão antecipada de falhas.

## 3. Origem e características dos dados

Os dados foram gerados pelo módulo:

`simulacao_industrial/gerador_dados.py`

Configuração principal:

| Parâmetro | Valor |
|---|---|
| Período simulado | 365 dias |
| Data inicial padrão | 01/01/2025 |
| Semente aleatória | 42 |
| Falhas simuladas | 33 |
| Registros utilizáveis após criação das variáveis históricas | 358 |
| Falhas nos registros utilizáveis | 32 |

O gerador considera relações simuladas entre operação, produção, temperatura, consumo energético e falhas.

Essas relações são hipóteses de engenharia utilizadas para construir o ambiente de aprendizagem. Não foram estimadas a partir de medições industriais reais.

## 4. Estratégia de validação

A separação dos dados respeitou a ordem cronológica, sem embaralhamento.

| Conjunto | Registros | Falhas |
|---|---:|---:|
| Treinamento | 250 | 24 |
| Validação | 54 | 4 |
| Teste reservado | 54 | 4 |
| **Total** | **358** | **32** |

O conjunto de treinamento foi utilizado para ajustar os modelos.

O ajuste de hiperparâmetros utilizou `TimeSeriesSplit` dentro do treinamento, com três divisões temporais.

O conjunto de validação foi utilizado para comparar os classificadores.

**O conjunto de teste permaneceu reservado e não foi utilizado para selecionar o modelo nesta etapa.**

A padronização da Regressão Logística foi realizada por meio de um `Pipeline`, ajustado exclusivamente sobre os dados de treinamento.

## 5. Modelos avaliados

### 5.1. Regressão Logística

Implementada com:

- `LogisticRegression`;
- `StandardScaler`;
- `class_weight="balanced"`;
- `max_iter=1000`;
- `random_state=42`.

O modelo fornece probabilidades de classificação e permite examinar coeficientes padronizados.

### 5.2. Árvore de Decisão

Configuração utilizada:

- `max_depth=4`;
- `min_samples_leaf=5`;
- `class_weight="balanced"`;
- `random_state=42`.

### 5.3. Random Forest

Configuração inicial:

- `n_estimators=100`;
- `max_depth=6`;
- `min_samples_leaf=3`;
- `class_weight="balanced"`;
- `random_state=42`.

### 5.4. Random Forest otimizada

A busca de hiperparâmetros utilizou `RandomizedSearchCV`, com validação temporal e otimização por recall.

Melhor configuração encontrada na execução registrada:

| Hiperparâmetro | Valor |
|---|---|
| `n_estimators` | 50 |
| `max_depth` | 3 |
| `min_samples_split` | 2 |
| `min_samples_leaf` | 5 |
| `max_features` | `log2` |

Recall médio na validação cruzada temporal: aproximadamente **0,573**.

## 6. Resultados comparativos

Resultados obtidos sobre os 54 registros de validação, incluindo quatro falhas:

| Modelo | Acurácia | Precisão | Recall | FP | FN | Custo simulado |
|---|---:|---:|---:|---:|---:|---:|
| Regressão Logística | 100,00% | 100,00% | 100% | 0 | 0 | R$ 0 |
| Árvore de Decisão | 74,07% | 18,75% | 75% | 13 | 1 | R$ 3.950 |
| Random Forest otimizada | 74,07% | 18,75% | 75% | 13 | 1 | R$ 3.950 |
| Random Forest original | 88,89% | 33,33% | 50% | 4 | 2 | R$ 4.600 |

A Regressão Logística identificou as quatro falhas do conjunto de validação sem gerar falsos alarmes nessa execução.

Entretanto, quatro ocorrências positivas são insuficientes para demonstrar confiabilidade estatística em operação real.

## 7. Função de custo financeiro

Para aproximar a avaliação técnica das prioridades do negócio, foi definida a função:

**Custo total = (FP × R$ 150) + (FN × R$ 2.000)**

Onde:

- **FP:** falso positivo — alarme emitido sem falha real;
- **FN:** falso negativo — falha existente não identificada.

Os valores são **hipóteses financeiras simuladas**, e não custos observados em uma fábrica.

O falso negativo recebeu um peso maior devido ao potencial de perdas operacionais, desperdícios, manutenção corretiva e interrupções de produção.

### 7.1. Interpretação econômica

A Random Forest otimizada reduziu o custo simulado de R$ 4.600 para R$ 3.950 em comparação com a versão original.

Isso corresponde a uma redução aproximada de **14,13%** no custo dos erros de classificação nesse conjunto de validação.

A melhoria ocorreu com redução de falsos negativos, apesar do aumento de falsos positivos.

O custo de R$ 0 da Regressão Logística representa somente a ausência de erros nesse conjunto de validação. **Não significa economia financeira comprovada, custo operacional zero ou retorno sobre investimento garantido.**

## 8. Importância das variáveis e interpretação

Na Random Forest original, as maiores importâncias por redução de impureza foram:

| Variável | Importância aproximada |
|---|---:|
| `consumo_kwh` | 0,3863 |
| `consumo_kwh_dia_anterior` | 0,1435 |
| `producao_unidades` | 0,1228 |
| `horas_operacao` | 0,1179 |
| `media_consumo_7d` | 0,1072 |
| `temperatura_ambiente_c` | 0,1008 |
| `turnos_planejados` | 0,0216 |

Essas importâncias descrevem o comportamento do modelo treinado, não relações causais comprovadas.

Variáveis correlacionadas podem compartilhar ou redistribuir a importância estimada.

## 9. Estabilidade e generalização

A Random Forest apresentou sensibilidade à semente aleatória utilizada no treinamento.

Nas cinco sementes avaliadas anteriormente, o recall variou entre 0,50 e 0,75, e o custo simulado variou entre R$ 2.600 e R$ 4.750.

Isso demonstra que o resultado depende, em parte, da configuração experimental e do pequeno número de falhas disponíveis para validação.

Também foi observada diferença entre o desempenho de treinamento e validação em modelos de árvores, indicando necessidade de investigar generalização e possível sobreajuste.

## 10. Calibração das probabilidades

Na avaliação preliminar da Regressão Logística foram obtidos:

- **Brier Score:** 0,015902;
- **Log Loss:** 0,121535;
- **Probabilidade média nos dias com falha:** 0,8162;
- **Probabilidade média nos dias normais:** 0,1066.

Esses indicadores são exploratórios.

O número reduzido de falhas impede concluir que as probabilidades estejam adequadamente calibradas.

O uso de `class_weight="balanced"` também deve ser considerado em avaliações futuras de calibração.

## 11. Decisão de engenharia

**Modelo selecionado provisoriamente: Regressão Logística.**

Justificativas:

1. Menor custo financeiro simulado no conjunto de validação.
2. Ausência de falsos negativos e falsos positivos na execução registrada.
3. Arquitetura relativamente simples e interpretável.
4. Menor complexidade de treinamento e manutenção em comparação com ensembles.
5. Possibilidade de examinar coeficientes e probabilidades.

Essa seleção não autoriza implantação em produção.

A decisão deverá ser reavaliada com novos períodos de dados, cenários de falhas mais variados, testes de robustez e, futuramente, dados industriais reais.

## 12. Model card — Regressão Logística

| Campo | Descrição |
|---|---|
| Nome | Classificador de Falhas Industriais — Regressão Logística |
| Projeto | AI Energy Auditor |
| Versão experimental | Semana 03 |
| Tipo | Classificação binária supervisionada |
| Objetivo | Detectar retrospectivamente falhas operacionais simuladas |
| Entrada | Sete variáveis operacionais e energéticas |
| Saída | Probabilidade estimada de falha e classificação binária |
| Origem dos dados | Gerador sintético desenvolvido no projeto |
| Avaliação | Separação cronológica e validação externa ao treinamento |
| Critério de escolha | Custo financeiro simulado, recall e precisão |
| Uso pretendido | Pesquisa, aprendizagem, prototipagem e comparação de modelos |
| Uso não recomendado | Decisões autônomas de manutenção, segurança ou paralisação industrial |

| Status | Protótipo experimental, não validado em produção |

### 12.1. Riscos conhecidos

- Dados sintéticos não representam integralmente a complexidade industrial.
- A falha simulada altera diretamente o consumo, tornando a classificação potencialmente mais simples que em cenários reais.
- Existem poucas falhas no conjunto de validação.
- As probabilidades ainda não possuem calibração robustamente demonstrada.
- O modelo não prevê falhas futuras.
- Os custos financeiros não foram validados com uma empresa.
- Mudanças de equipamentos, turnos, processos e sazonalidade podem reduzir o desempenho.

### 12.2. Supervisão humana

Qualquer uso industrial futuro deverá prever validação de dados, acompanhamento de desempenho, registro de decisões e supervisão por profissionais responsáveis pela operação.

## 13. Qualidade de software e testes

Foram implementados testes automatizados para:

- geração de dados sintéticos;
- integridade dos dados;
- criação de variáveis históricas sem vazamento;
- classificação de falhas;
- cálculo de custos;
- treinamento de classificadores;
- busca de hiperparâmetros;
- geração e ordenação do relatório comparativo;
- rejeição de entradas inválidas;
- funcionalidades anteriores da API e do projeto.

**Resultado da suíte completa:** 67 testes aprovados, sem falhas, em 10,70 segundos.

Foi observado um aviso de depreciação relacionado às dependências de teste do FastAPI/Starlette, sem falha de execução.

**Integração contínua:** GitHub Actions `Testes Python #17` aprovado para o commit `662f363`.

## 14. Artefatos entregues

Principais arquivos desenvolvidos ou utilizados durante a Semana 03:

| Arquivo | Finalidade |
|---|---|
| `notebooks/semana03_dia11_formulacao_problema.ipynb` | Formulação do problema |
| `simulacao_industrial/gerador_dados.py` | Simulação de dados e falhas |
| `simulacao_industrial/custos_falhas.py` | Função de custo financeiro |
| `simulacao_industrial/classificador_falhas.py` | Preparação, treinamento e avaliação |
| `simulacao_industrial/comparador_modelos.py` | Comparação de três estimadores |
| `simulacao_industrial/ajuste_hiperparametros.py` | Ajuste temporal com RandomizedSearchCV |
| `simulacao_industrial/relatorio_comparador.py` | Relatório executável dos quatro modelos |
| `testes/test_relatorio_comparador.py` | Testes automatizados do comparador |
| `relatorios/semana03_relatorio_modelos.md` | Relatório técnico e model card |

## 15. Limitações da entrega

O sistema demonstra uma metodologia de desenvolvimento e avaliação de modelos de classificação, mas ainda não representa uma solução industrial pronta para comercialização.

As principais limitações são:

1. Dependência de dados simulados.
2. Ausência de avaliação com equipamentos e processos industriais reais.
3. Baixo número de falhas observadas na validação.
4. Ausência de validação final sobre o conjunto de teste reservado.
5. Falta de avaliação de custos reais de inspeção e manutenção.
6. Ausência de monitoramento contínuo de degradação do modelo.
7. Ausência de comprovação de capacidade de previsão antecipada.

## 16. Próximas melhorias

Para a continuidade do AI Energy Auditor, recomenda-se:

1. Construir cenários sintéticos mais variados, incluindo falhas discretas e alterações de comportamento energético.
2. Investigar desbalanceamento de classes e estratégias de calibração.
3. Avaliar modelos em períodos temporais adicionais.
4. Manter o conjunto de teste reservado até a etapa apropriada de avaliação final.
5. Incorporar dados industriais reais quando houver autorização e disponibilidade.
6. Separar claramente os objetivos de detecção de falhas, previsão de consumo e previsão antecipada de falhas.
7. Evoluir a solução para um MVP demonstrável com monitoramento e supervisão humana.

## 17. Conclusão

A Semana 03 consolidou o desenvolvimento de um comparador de modelos de Machine Learning para detecção retrospectiva de falhas industriais.

Foram implementados quatro classificadores, uma estratégia de validação temporal, uma função de custo financeiro simulado e testes automatizados integrados ao GitHub Actions.

A Regressão Logística foi selecionada provisoriamente por apresentar o melhor resultado no conjunto de validação estudado.

**A principal conclusão de engenharia é que a escolha de um modelo deve considerar não apenas a acurácia, mas também os custos dos erros, a estabilidade, a interpretabilidade e os limites dos dados disponíveis.**

O projeto permanece em fase experimental e seguirá evoluindo dentro do curso de Engenharia de Inteligência Artificial.
