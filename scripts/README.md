[Inicio](../README.md) | [Data](../data/README.md) | [Features](../features/README.md) | [Notebooks](../notebooks/README.md) | **<u>Scripts</u>** | [Reports](../reports/README.md) | [Interactive Reports](../interactive_reports/README.md) | [Dashboard](../dashboard/) | [Models](../models/README.md) | [Metrics](../metrics/README.md)

# Scripts

A pasta ```scripts/``` contém os arquivos responsáveis pelo processamento de dados, engenharia de features, modelagem e funções utilitárias que são usadas em todo o pipeline do projeto.

## ```pre_processing.py```

Responsável pelo pré-processamento dos dados brutos, incluindo:

- Limpeza de dados (remoção de valores nulos, duplicados ou inconsistentes)
- Normalização e padronização de variáveis numéricas
- Conversão de tipos de dados
- Tratamento de valores categóricos

## ```utils.py```

Arquivo de funções utilitárias para facilitar operações comuns no projeto, como:

- Funções de leitura e escrita de arquivos
- Transformações genéricas de dados
- Métricas customizadas
- Helpers de visualização

## ```features.py```

Contém funções de engenharia de features, incluindo:

- Criação de novas variáveis derivadas
- Seleção de features importantes
- Transformações específicas para preparar os dados para modelagem

## ```modeling.py```

Responsável por toda a parte de modelagem, incluindo:

- Treinamento de modelos preditivos
- Avaliação de performance com métricas apropriadas
- Salvar e carregar modelos treinados
- Testes de hiperparâmetros e validação cruzada