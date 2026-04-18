[Inicio](../README.md) | [Data](../data/README.md) | [Features](../features/README.md) | **<u>Notebooks</u>** | [Scripts](../scripts/README.md) | [Reports](../reports/README.md) | [Interactive Reports](../interactive_reports/README.md) | [Dashboard](../dashboard/) | [Models](../models/README.md) | [Metrics](../metrics/README.md) | [API](../api/README.md)

# Notebooks Usados


## 1_pre_processamento.ipynb

Este notebook é responsável pela limpeza e padronização dos dados brutos recebidos via API e denúncias dos usuários. Ele lida com a tipagem das variáveis, tratamento de valores ausentes e a formatação rigorosa das coordenadas geográficas para garantir que a localização da ocorrência seja precisa. Aqui também é implementada a lógica de criptografia de senhas e segurança dos dados dos usuários.

## 2_eda.ipynb

Focado na Análise Exploratória de Dados, este notebook extrai os insights necessários para alimentar a Página de Histórico e os Indicadores da Home. Ele analisa a distribuição das queimadas por cidade no Norte de Minas, identifica a média de intensidade dos focos (baixa, média ou alta) e estuda o volume de denúncias ao longo do tempo (30, 60 e 90 dias) para validar os critérios de sucesso do monitoramento.

## 3_feature_engineering.ipynb

Este notebook cria as variáveis inteligentes que sustentam as regras de negócio do sistema. O destaque é a criação do algoritmo de Cluster de Mapa, que agrupa focos próximos para otimizar a visualização. Além disso, desenvolve a lógica de Validação Automática, que transforma denúncias individuais em um "alerta validado" caso três registros ocorram na mesma área, e calcula o Nível de Risco da região com base na densidade de focos ativos.

## 4_ai.ipynb

Destinado à inteligência analítica e modelos preditivos, este notebook implementa modelos de Machine Learning para análise e previsão de queimadas em Minas Gerais. Os modelos utilizam dados históricos de focos de queimada e variáveis meteorológicas para auxiliar na tomada de decisão operacional.

### Modelos Implementados:

1. **LightGBM - Classificação de Intensidade de Queimadas**
   - **Função**: Classifica a intensidade dos focos de queimada em três categorias (Baixo, Médio, Alto) com base no Fire Radiative Power (FRP). Utiliza cortes definidos: Baixo (<15 FRP), Médio (15-80 FRP), Alto (>80 FRP).
   - **Objetivo**: Auxiliar na priorização de recursos de combate a incêndios, identificando focos de alta intensidade que requerem atenção imediata.
   - **Features Utilizadas**: Satelite, Nome_Município, Bioma, DiaSemChuva, Precipitacao, Latitude, Longitude, Mes, Hora_decimal, ID_Município.
   - **Configuração**: Modelo multiclasse com balanceamento de classes, early stopping e avaliação em dados de 2025.

2. **LightGBM - Classificação de Risco de Fogo**
   - **Função**: Classifica o risco de ocorrência de fogo em binário (Sem Fogo ou Fogo) com base na variável RiscoFogo (binarizada em >0.5).
   - **Objetivo**: Prever áreas com alto risco de incêndio para prevenção e monitoramento proativo.
   - **Features Utilizadas**: Satelite, Nome_Município, Bioma, DiaSemChuva, Precipitacao, Latitude, Longitude, Mes, Hora_decimal, ID_Município.
   - **Configuração**: Modelo binário com early stopping, otimizado para grandes volumes de dados.

Os modelos são treinados com dados históricos (2022-2024) e avaliados em dados de 2025, garantindo uma divisão cronológica para evitar data leakage. Inclui visualizações como matrizes de confusão, mapas de distribuição geográfica e análises sazonais para validar o desempenho.