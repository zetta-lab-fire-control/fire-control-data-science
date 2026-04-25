[Inicio](../README.md) | [Data](../data/README.md) | [Features](../features/README.md) | [Notebooks](../notebooks/README.md) | [Scripts](../scripts/README.md) | [Reports](../reports/README.md) | [Interactive Reports](../interactive_reports/README.md) | [Dashboard](../dashboard/README.md) | **<u>Models</u>** | [Metrics](../metrics/README.md) | [API](../api/README.md)

# Models

Repositório contendo todos os modelos de Machine Learning treinados para o projeto de **Combate e Prevenção de Incêndios**. Os modelos utilizam dados de queimadas e condições climáticas para classificar intensidade e prever riscos de fogo em Minas Gerais.

## Índice

- [Visão Geral](#visão-geral)
- [Modelos Disponíveis](#modelos-disponíveis)
  - [1. Classificador de Intensidade de Queimadas](#1-classificador-de-intensidade-de-queimadas)
  - [2. Preditor de Risco de Fogo](#2-preditor-de-risco-de-fogo)
  - [3. Scaler de Normalização](#3-scaler-de-normalização)
- [Características Utilizadas](#características-utilizadas)
- [Dados de Treinamento](#dados-de-treinamento)
- [Como Usar os Modelos](#como-usar-os-modelos)
- [Arquitetura Técnica](#arquitetura-técnica)

---

## Visão Geral

O projeto implementa **dois modelos principais** de Machine Learning baseados em **LightGBM** para:

1. **Classificação** de intensidade de queimadas (Baixa, Média, Alta)
2. **Regressão** para predição contínua de risco de fogo (0-1)

Ambos os modelos foram treinados em dados históricos (2022-2024) e validados em dados recentes (2025), respeitando a cronologia dos dados para evitar data leakage.

---

## Modelos Disponíveis

### 1. Classificador de Intensidade de Queimadas

**Arquivo:** `modelo_intensidade_queimadas_mg.joblib`

#### Descrição
Classifica focos de incêndio em **três níveis de intensidade** com base no valor de FRP (Fire Radiative Power), um indicador de potência radiativa do fogo captado por satélites.

#### Categorias de Saída
| Nível | Classificação | Intervalo FRP (MW) |
|-------|---------------|-------------------|
| 0     | **Baixo** | < 15 MW |
| 1     | **Médio** | 15 - 80 MW |
| 2     | **Alto** | > 80 MW |

#### Hiperparâmetros
```python
LGBMClassifier(
    objective='multiclass',
    num_class=3,
    n_estimators=1500,           # Número de árvores
    learning_rate=0.05,          # Taxa de aprendizado
    num_leaves=64,               # Máximo de folhas por árvore
    class_weight='balanced',     # Ponderação para desbalanceamento de classes
    importance_type='gain',      # Tipo de importância das features
    random_state=42
)
```

#### Métricas de Desempenho
| Métrica | Valor |
|---------|-------|
| **Acurácia Global** | 70.09% |
| **Precisão (Macro)** | 62.35% |
| **Recall (Macro)** | 48.21% |
| **F1-Score (Macro)** | 44.54% |
| **ROC-AUC** | - |

#### Desempenho por Classe
| Classe | Precisão | Recall | F1-Score | Suporte |
|--------|----------|--------|----------|---------|
| Baixo | 0.886 | 0.818 | 0.850 | 4,910,905 |
| Médio | 0.314 | 0.588 | 0.410 | 1,158,459 |
| Alto | 0.670 | 0.040 | 0.076 | 670,101 |

#### Matriz de Confusão
```
                  Predito
            Baixo  Médio  Alto
Real Baixo  4,015,232  891,477  4,196
     Médio  467,678  681,718  9,063
     Alto   48,515  594,689  26,897
```

#### Interpretação
- O modelo **identifica bem** focos com intensidade baixa (recall 81.8%)
- Apresenta **dificuldade** em detectar eventos de intensidade muito alta (recall 4%)
- A classe "Médio" é bem detectada mas com precisão moderada

#### Casos de Uso
✅ Triagem rápida de eventos críticos vs. eventos menores  
✅ Análise de sazonalidade de incêndios  
✅ Priorização de recursos de combate baseado em intensidade  
⚠️ Não recomendado como único critério para alertas de emergência de classe Alta

---

### 2. Preditor de Risco de Fogo

**Arquivo:** `preditor_risco_fogo.joblib`

#### Descrição
Modelo de **regressão** que prediz continuamente o **nível de risco de fogo** (escala 0-1) com base em variáveis climáticas, geográficas e temporais. O alvo é o índice **RiscoFogo** normalizado via MinMaxScaler.

#### Saída
- **Intervalo:** 0.0 a 1.0
- **Interpretação:** 0 = Risco Mínimo | 1 = Risco Máximo

#### Hiperparâmetros
```python
LGBMRegressor(
    objective='regression',
    n_estimators=3000,           # Aumentado para melhor generalização
    learning_rate=0.03,          # Aprendizado refinado
    num_leaves=128,              # Mais complexidade para capturar padrões
    max_depth=-1,                # Profundidade ilimitada
    min_child_samples=20,        # Mínimo de amostras por folha
    random_state=42,
    importance_type='gain'
)
```

#### Métricas de Desempenho
| Métrica | Valor |
|---------|-------|
| **MAE** (Erro Médio Absoluto) | 0.1034 |
| **MSE** (Erro Quadrático Médio) | 0.0326 |
| **RMSE** (Raiz do Erro Quadrático) | 0.1805 |
| **R² Score** | 0.6549 (65.49%) |
| **MAPE** | Não aplicável (y_test contém zeros) |

#### Interpretação das Métricas
- **R² = 0.6549:** O modelo explica ~65% da variância no risco de fogo
- **MAE = 0.1034:** Em média, as predições diferem em ±0.10 na escala 0-1
- **RMSE = 0.1805:** Mais sensível a erros grandes; indica alguns outliers

#### Features de Maior Importância
```
Top 5 Atributos Influenciadores:
1. ID_Município (relevância geográfica)
2. Nome_Município (microclima local)
3. DiaSemChuva (tendência de seca)
4. Precipitacao (inibidor de fogo)
5. Hora_decimal (pico de calor diário)
```

#### Casos de Uso
✅ Previsão de risco para despacho de recursos  
✅ Alertas automáticos graduados por intensidade  
✅ Análise de tendências e padrões sazonais  
✅ Integração com dashboards em tempo real  

---

### 3. Scaler de Normalização

**Arquivo:** `scaler_risco.joblib`

#### Descrição
Objeto **MinMaxScaler** do scikit-learn que normaliza o índice **RiscoFogo** original para a escala 0-1.

#### Propósito
- Transforma dados brutos de risco (que podem estar em escalas variadas) para 0-1
- Essencial para o modelo de regressão funcionar corretamente
- Deve ser aplicado **antes** de fazer predições na API

#### Uso
```python
import joblib
import numpy as np

# Carregar o scaler
scaler = joblib.load('scaler_risco.joblib')

# Normalizar um valor
risco_original = 42.5  # Escala original
risco_normalizado = scaler.transform([[risco_original]])

# Desnormalizar uma predição do modelo
risco_predito_normalizado = 0.65
risco_original = scaler.inverse_transform([[risco_predito_normalizado]])
```

---

## Características Utilizadas

Todos os modelos utilizam as mesmas **10 features** para manter consistência:

| # | Feature | Tipo | Descrição |
|---|---------|------|-----------|
| 1 | **Satelite** | Categórica | Satélite que detectou o foco (GOES-16, MODIS, etc.) |
| 2 | **Nome_Município** | Categórica | Município onde o incêndio ocorreu |
| 3 | **Bioma** | Categórica | Tipo de bioma (Cerrado, Mata Atlântica, Caatinga, etc.) |
| 4 | **DiaSemChuva** | Numérica | Dias sem precipitação antes do evento |
| 5 | **Precipitacao** | Numérica | Quantidade de chuva (mm) |
| 6 | **Latitude** | Numérica | Coordenada Y geográfica |
| 7 | **Longitude** | Numérica | Coordenada X geográfica |
| 8 | **Mes** | Numérica | Mês do ano (1-12) |
| 9 | **Hora_decimal** | Numérica | Hora do dia em formato decimal (0-24) |
| 10 | **ID_Município** | Numérica | ID numérico do município |

---

## Dados de Treinamento

### Período de Dados
- **Treino:** 2022-01-01 a 2024-12-31 (3 anos)
- **Teste:** 2025-01-01 a 2025-12-31 (validação recente)
- **Total de Registros:** 6,739,465 (dados de teste)

### Fonte dos Dados
Os dados vêm de:
- **Satélites de Detecção:** GOES-16, MODIS (NASA)
- **Dados Climáticos:** Estações meteorológicas de MG
- **Base de Queimadas:** BD Queimadas INPE

### Tratamento de Dados
✅ Remoção de valores negativos de FRP  
✅ Normalização de variáveis contínuas (MinMaxScaler)  
✅ Codificação de variáveis categóricas para formato category do pandas  
✅ Otimização de tipos de dados para reduzir uso de memória  

---

## Como Usar os Modelos

### Carregamento na API
```python
from scripts.modeling import carregar_modelo_e_info, load_joblib
import joblib

# Opção 1: Carregar modelo com metadados
modelo_intensidade, info = carregar_modelo_e_info('modelo_intensidade_queimadas_mg.joblib')
modelo_risco, info = carregar_modelo_e_info('preditor_risco_fogo.joblib')

# Opção 2: Carregar apenas o modelo
modelo = load_joblib('modelo_intensidade_queimadas_mg.joblib')

# Carregar scaler
scaler = joblib.load('scaler_risco.joblib')
```

### Fazer Predições
```python
import pandas as pd

# Preparar dados (X_novo deve ter as 10 features)
features_necessarias = [
    'Satelite', 'Nome_Município', 'Bioma', 'DiaSemChuva', 
    'Precipitacao', 'Latitude', 'Longitude', 'Mes', 'Hora_decimal', 'ID_Município'
]

# Classificação de Intensidade
y_pred_classe = modelo_intensidade.predict(X_novo)  # Retorna [0, 1, 2]
y_pred_proba = modelo_intensidade.predict_proba(X_novo)  # Retorna probabilidades

# Regressão de Risco
y_pred_risco_normalizado = modelo_risco.predict(X_novo)  # Retorna [0-1]
y_pred_risco_original = scaler.inverse_transform(y_pred_risco_normalizado)  # Denormaliza
```

### Integração com FastAPI
Veja o arquivo `api/main.py` para exemplos de endpoints que utilizam estes modelos.

---

## Arquitetura Técnica

### Formato de Armazenamento
- **Formato:** joblib (eficiente para objetos sklearn)
- **Tamanho Típico:** ~500KB por modelo
- **Serialização:** Inclui metadados (features, classes, tamanho) no mesmo arquivo

### Pipeline de Treinamento
```
1. Carregamento de dados (parquet)
2. Limpeza e validação
3. Normalização (MinMaxScaler para RiscoFogo)
4. Divisão Treino/Teste (respeitando cronologia)
5. Codificação de categóricas
6. Treinamento LightGBM
7. Salvamento com metadados
8. Cálculo de métricas
```

### Consistência Entre Modelos
- ✅ Mesmas features em ambos os modelos
- ✅ Mesmo período de treinamento
- ✅ Mesmo scaler de normalização
- ✅ Código centralizado em `scripts/modeling.py`

### Monitoramento em Produção
Recomenda-se acompanhar:
- Distribuição de predições (comparar com treino)
- Taxa de erros acima de MAE para regressão
- Classe mais frequentemente predita para classificação
- Degradação de performance ao longo do tempo

---

## Referências

- **Framework:** LightGBM (Gradient Boosting)
- **Linguagem:** Python 3.11+
- **Dependências:** lightgbm, scikit-learn, pandas, numpy, joblib
- **Notebooks de Origem:** `notebooks/4_ai.ipynb`
- **Script de Modelagem:** `scripts/modeling.py`

---

**Última Atualização:** Janeiro 2025  
**Status:** ✅ Em Produção  
**Acesso Autorizado:** Equipe de Data Science
