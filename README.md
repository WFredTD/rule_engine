🚀 RULE ENGINE - PROVA DE CONCEITO DE VALIDAÇÃO DINÂMICA
========================================================

Bem-vindo ao repositório do **Rule Engine**, um projeto focado na construção de um *backend* robusto para **validação dinâmica de regras de negócio**.

Este projeto integra os fundamentos da **Fase 1 da minha Trilha de Desenvolvimento**, demonstrando domínio em arquitetura, modelagem de dados e lógica Python essencial, com uma visão clara de futuro Micro-SaaS.

🌟 Sobre a Trilha de Estudo (Contexto)
--------------------------------------

Este projeto integra os conceitos dos Módulos 1, 2 e 3 da minha trilha de estudo documentada. Ele serve como o Projeto Integrador (PI) desta fase de aprendizado.

-   **Acesse minha Trilha de Estudo Completa [aqui](ttps://ebony-sphere-7b6.notion.site/Trilha-para-Desenvolvimento-de-Software-20edac67d6178099af40c363dfb90e7a)** 
- **Acesse os exercícios minha Trilha [aqui](https://github.com/WFredTD/trilha-desenvolvimento-de-software)** 

## 🚀 Tecnologias Utilizadas

<p align="center">
  <img loading="lazy" src="https://skillicons.dev/icons?i=python,postgresql,docker,vscode,git,github" alt="Tech Stack"><br>
  <img loading="lazy" src="https://img.shields.io/badge/dotenv-FDC100?style=for-the-badge&logo=none&logoColor=black" alt="Python-DotEnv">
  <img loading="lazy" src="https://img.shields.io/badge/Black-000000?style=for-the-badge&logo=python&logoColor=white" alt="Black Formatter">
  <img loading="lazy" src="https://img.shields.io/badge/isort-1C3D5A?style=for-the-badge&logo=python&logoColor=white" alt="isort">
</p>

💡 Valor e Arquitetura do Projeto
---------------------------------

Este projeto é uma **Prova de Conceito (PoC)** de alto valor, pois implementa a **Inversão de Controle (IoC)**, permitindo que as regras de validação sejam definidas e alteradas via banco de dados, sem a necessidade de modificar ou fazer *deploy* de código.

### 🔑 Habilidades Técnicas em Destaque

| Habilidade | Módulo | Demonstração no Código |
| --- | --- | --- |
| **POO Avançada/IoC** | Python Essencial | Uso do **`import operator`** para mapeamento dinâmico de lógica (`RuleEngine.validate()`). |
| **Modelagem Segura** | SQL Essencial | Uso de **`UUID PRIMARY KEY`** e **`FOREIGN KEY`** (garantindo integridade referencial). |
| **Infraestrutura** | Conteinerização (Adiantado) | Ambiente de desenvolvimento completo com **Docker Compose** e **PostgreSQL**. |
| **Conectividade** | Python Essencial | Comunicação direta e segura com o DB via **Psycopg2** (previne SQL Injection). |


### 📂 Estrutura de Diretórios

```
rule_engine/
├── .env              # Variáveis de ambiente (IGNORADO via .gitignore)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── rule-engine/      # Pacote Python
    ├── __init__.py
    ├── database.py   # POO + SQL DDL/DML/DQL
    └── rule_engine.py # CLASSE CORE (POO + Lógica de Comparação)

```

| Arquivo/Pasta | Função |
| --- | --- |
| `docker-compose.yml` | Orquestra os serviços (`app` Python e `db` PostgreSQL). |
| `Dockerfile` | Define o ambiente Python da aplicação (`app`). |
| `.env` / `.gitignore` | Gerenciamento seguro de credenciais. |
| `rule-engine/` | Pacote Python principal da aplicação. |
| `rule-engine/database.py` | Gerencia a **Conexão** e executa o **DDL** (`CREATE TABLE`) e **DQL** (`SELECT`) com SQL Puro. |
| `rule-engine/rule_engine.py` | Contém a classe **`RuleEngine`** (a lógica de validação central). |

⚙️ Setup Local e Execução
-------------------------

Este projeto utiliza **Docker Compose** para garantir um ambiente idêntico de desenvolvimento e produção.

### Pré-requisitos

-   **Docker Desktop** (rodando)

-   **Git**

### Passos para Rodar o Projeto

1.  **Clone o Repositório:**


    ```
    git clone https://github.com/WFredTD/rule_engine.git
    cd rule_engine

    ```

2.  **Configuração do Ambiente:** Crie o arquivo `.env` na raiz do projeto com as credenciais do PostgreSQL.

3.  **Execução:** Inicie os serviços, construa a imagem Python e execute o script de teste:


    ```
    # O comando executa o DDL (criação de tabelas) e o teste de validação de dados
    docker compose up --build

    ```

    *A saída do console confirmará a criação das tabelas e exibirá a falha de validação simulada, comprovando que o motor está funcional.*



📧 Contato
----------

<div>
    <a href = "mailto:fredtorresdreyer@gmail.com"><img loading="lazy" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
    <a href="https://www.linkedin.com/in/walterftdreyer/" target="_blank"><img loading="lazy" src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
</div>