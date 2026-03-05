# Guia de Contribuições

Este documento descreve como cada área pode contribuir para o projeto e quais são as regras gerais de organização, nomenclatura de branch e boas práticas.

## Área do Projeto

- **Comunicação e Marketing**:
- **Ciência e Governança de Dados**:
- **Desenvolvimento de Software**:
- **Geotecnologia**:
- **Gestão de Projetos**:
- **Design de Soluções**:

## Regras Gerais

### 1. Padronização de Branches

#### 1.1 Uso de Prefixos

Ao criar uma nova branch, deve-se colocar um prefixo que explique seu propósito. Abaixo estão prefixos comuns:

- **feature/**: Adição de novos componentes ou funcionalidades.
- **bugfix/**: Correção de bugs ou erros no código.
- **hotfix/**: Aplicação de correções urgentes, geralmente em produção.
- **design/**: Focado na interface ou experiência do usuário.
- **refactor/**: Melhora de estrutura de código sem alterar a funcionalidade.
- **test/**: Para escrita e melhoria de testes automaticos.
- **doc/**: Atualização de documentos.

<img src="https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F68kturf7t2eg7nufsyws.png" width="500" height="600">

Exemplos de uso de prefixo incluem:

- ```feature/user-authentication```
- ```bugfix/fix-login-error```
- ```hotfix/urgent-patch-crash```
- ```design/update-navbar```
- ```refactor/remove-unused-code```
- ```test/add-unit-tests```
- ```doc/update-readme```

#### 1.2 Manter nomes curtos e descritivos

Nomes de Branches devem ser consisos e informativos. Um bom nome de branch deve descrever o que é sem ser longo ou vago. Recomendações incluem:

- Usar hipens (```-```) a fim de separar palavras para melhor leitura.
- Evitar termos genéricos como ```atualização```, ```mudanças```, ou ```coisa```.
- Focar na tarefa ou issue principal da branch.

<img src="https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F8bzblesluvtrl0y7aefh.png" width="500" height="600">

#### **Exemplos de nomes de branches**

##### **1. Feature**
- ```feature/add-user-profile```
- ```feature/implement-chat-notifications```

##### **2. Bug Fixes**
- ```bugfix/correct-date-display```
- ```bugfix/fix-404-error```

##### **3. Design Updates**
- ```design/improve-dashboard-ui```
- ```design/revise-mobile-layout```

##### **4. Refactoring**
- ```refactor/optimize-database-queries```
- ```refactor/simplify-api-routes```

##### **5. Hotfixes**
- ```hotfix/security-patch```
- ```hotfix/fix-login-issue```

##### **6. Documentation**
- ```doc/add-api-instructions```
- ```doc/update-contributor-guidelines```

### 2. Padronização de Commits

Devera ser utilizado o padrão Conventional Commits, esses que definem um conjunto de regras para criar um histórico de commit explícito, o que facilita a criação de ferramentas automatizadas.

Esses commits auxiliarão você e sua equipe a entenderem de forma facilitada quais alterações foram realizadas no trecho de código que foi commitado.

Essa identificação ocorre por meio de uma palavra e emoji que identifica se aquele commit realizado se trata de uma alteração de código, atualização de pacotes, documentação, alteração de visual, teste...

### 2.1 Tipo e Descrição

O commit semântico possui os elementos estruturais abaixo (tipos), que informam a intenção do seu commit ao utilizador(a) de seu código.

- ```feat``` - Commits do tipo feat indicam que seu trecho de código está incluindo um novo recurso (se relaciona com o MINOR do versionamento semântico).
- ```fix``` - Commits do tipo fix indicam que seu trecho de código commitado está solucionando um problema (bug fix), (se relaciona com o PATCH do versionamento semântico).
- ```docs``` - Commits do tipo docs indicam que houveram mudanças na documentação, como por exemplo no Readme do seu repositório. (Não inclui alterações em código).
- ```test``` - Commits do tipo test são utilizados quando são realizadas alterações em testes, seja criando, alterando ou excluindo testes unitários. (Não inclui alterações em código)
- ```build``` - Commits do tipo build são utilizados quando são realizadas modificações em arquivos de build e dependências.
- ```perf``` - Commits do tipo perf servem para identificar quaisquer alterações de código que estejam relacionadas a performance.
- ```style``` - Commits do tipo style indicam que houveram alterações referentes a formatações de código, semicolons, trailing spaces, lint... (Não inclui alterações em código).
- ```refactor``` - Commits do tipo refactor referem-se a mudanças devido a refatorações que não alterem sua funcionalidade, como por exemplo, uma alteração no formato como é processada determinada parte da tela, mas que manteve a mesma funcionalidade, ou melhorias de performance devido a um code review.
- ```chore``` - Commits do tipo chore indicam atualizações de tarefas de build, configurações de administrador, pacotes... como por exemplo adicionar um pacote no gitignore. (Não inclui alterações em código)
- ```ci``` - Commits do tipo ci indicam mudanças relacionadas a integração contínua (continuous integration).
- ```raw``` - Commits do tipo raw indicam mudanças relacionadas a arquivos de configurações, dados, features, parâmetros.
- ```cleanup``` - Commits do tipo cleanup são utilizados para remover código comentado, trechos desnecessários ou qualquer outra forma de limpeza do código-fonte, visando aprimorar sua legibilidade e manutenibilidade.
- ```remove``` - Commits do tipo remove indicam a exclusão de arquivos, diretórios ou funcionalidades obsoletas ou não utilizadas, reduzindo o tamanho e a complexidade do projeto e mantendo-o mais organizado.

## Referencial Teórico

Abaixo são as informações originais para os tipos de commit e versionamento:

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Versionamento Semântico](https://semver.org/)
- [Github Branching Name Best Practices](https://dev.to/jps27cse/github-branching-name-best-practices-49ei)
