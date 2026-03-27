[Inicio](../README.md) | **<u>Data</u>** | [Features](../features/README.md) | [Notebooks](../notebooks/README.md) | [Scripts](../scripts/README.md) | [Reports](../reports/README.md) | [Interactive Reports](../interactive_reports/README.md) | [Dashboard](../dashboard/README.md) | [Models](../models/README.md) | [Metrics](../metrics/README.md) | [API](../api/README.md)

# Descrições de Dados e Informações

## Indice

- [Dados Estruturados](#dados-estruturados)
  - [Area Territoriais - IBGE](#areas-territoriais---ibge)
  - [Código de Múnicipios IBGE](#código-de-múnicipios-ibge)
  - [BDQUEIMADAS](#bdqueimadas)
  - [BDMEP - Base dos Dados](#bdmep---base-dos-dados)
  - [MapBiomas](#mapbiomas)
  - [TerraBrasilis INPE](#terrabrasilis-inpe)
- [Dados Não-Estruturados](#dados-não-estruturados)

## Datasets Utilizados

### Dados Estruturados

#### [Areas Territoriais - IBGE](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html?t=acesso-ao-produto&c=1)

O redimensionamento dos valores de áreas é próprio da evolução das geotecnologias aplicadas no monitoramento da dinâmica da divisão territorial brasileira, que implica na atualização periódica dos valores das áreas estaduais e municipais com a utilização continuada de melhores técnicas e de melhores insumos de produção, além de refletir as eventuais alterações nos limites político-administrativos por justificativas legais ou judiciais.

O cálculo da área territorial do Brasil em 2024, resultou no valor total de 8509379,576 km².

Considerando a vasta quantidade de dados que o dataset oferece, será focado apenas num grupo selecionado de atributos para o projeto, tendo em mente o foco á nível estadual e municipal.

<details>
  <summary>Clique para ver o 'Dicionário de Dados: Areas Territóriais - IBGE'</summary>
  <table border="1" cellspacing="0" cellpadding="5">
    <thead>
      <tr>
        <th>Coluna</th>
        <th>Tipo</th>
        <th>Descrição</th>
        <th>Unidade / Formato</th>
        <th>Classificação</th>
        <th>Valores possíveis / Exemplo</th>
        <th>Observações</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>ID_UF</td>
        <td>Inteiro</td>
        <td>Identificador único de cada UF (Unidade Federal / Estado)</td>
        <td>N/A</td>
        <td>Dados Brutos</td>
        <td>11, 12, 13, ...</td>
        <td>Identificador é composto de apenas dois caracteres.</td>
      </tr>
    </tbody>
  </table>
</details>

#### [Código de Múnicipios IBGE](https://www.ibge.gov.br/explica/codigos-dos-municipios.php)

A Tabela de Códigos de Municípios do IBGE apresenta a lista dos municípios brasileiros associados a um código composto de 7 dígitos, sendo os dois primeiros referentes ao código da Unidade da Federação.
O propósito dessa tabela é de integrar a vasta quantidade de dados a partir dos códigos identificadores dos UFs e Munícipios.

<details>
  <summary>Clique para ver o 'Dicionário de Dados - Código de Múnicipios IBGE'</summary>
  <table border="1" cellspacing="0" cellpadding="5">
    <thead>
      <tr>
        <th>Coluna</th>
        <th>Tipo</th>
        <th>Descrição</th>
        <th>Unidade / Formato</th>
        <th>Classificação</th>
        <th>Valores possíveis / Exemplo</th>
        <th>Observações</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>ID_UF</td>
        <td>Inteiro</td>
        <td>Identificador único de cada UF (Unidade Federal / Estado)</td>
        <td>N/A</td>
        <td>Dados Brutos</td>
        <td>11, 12, 13, ...</td>
        <td>Identificador é composto de apenas dois caracteres.</td>
      </tr>
      <tr>
        <td>Nome_UF</td>
        <td>String</td>
        <td>Nome do UF (Unidade Federal / Estado)</td>
        <td>N/A</td>
        <td>Dados Brutos</td>
        <td>Tocantins, Minas Gerais, Acre, etc.</td>
        <td>Há 27 UFs (26 Estados e 1 Distrito Federal)</td>
      </tr>
      <tr>
        <td>ID_MUN</td>
        <td>Inteiro</td>
        <td>Latitude do ponto de ocorrência</td>
        <td>N/A</td>
        <td>Dados Brutos</td>
        <td>1100346, 1100023, 1100601, entre outros.</td>
        <td>O identificador é composto de 7 caracteres. A qual os primeiros dois utiliza-se o ID_UF.</td>
      </tr>
      <tr>
        <td>Nome_MUN</td>
        <td>String</td>
        <td>Nome do Município.</td>
        <td>N/A</td>
        <td>Dados Brutos</td>
        <td>Arame, Bacuri, Xambioá, etc.</td>
        <td>Existem 5.569 ou 5.570 municípios</td>
      </tr>
    </tbody>
  </table>
</details>

#### [TerraBrasilis INPE](https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/)

##### [TerraBrasilis INPE - Situação Atual](https://terrabrasilis.dpi.inpe.br/queimadas/situacao-atual/situacao_atual/)



##### [TerraBrasilis INPE - BDQUEIMADAS](https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/)



#### [Banco de Dados de Queimadas - BaseDosDados](https://basedosdados.org/datasetf06f3cdc-b539-409b-b311-1ff8878fb8d9?table=a3696dc2-4dd1-4f7e-9769-6aa16a1556b8)



### Dados Não Estruturados
