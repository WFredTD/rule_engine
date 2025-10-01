🚀 SAAS RULE ENGINE - PROOF OF CONCEPT (POC)
============================================

**Status:** Fase 1 Concluída (Core Logic) | **Próximo Passo:** Integração com Django (API)

1\. Visão Geral e Objetivo de Negócio
-------------------------------------

Este projeto é a Prova de Conceito (PoC) de um **Micro-SaaS de Validação de Regras de Negócio Dinâmicas**.

### 🎯 Objetivo Principal

Permitir que as regras de negócio de um cliente (ex: "idade mínima", "desconto máximo") sejam definidas e alteradas **diretamente no banco de dados**, eliminando a necessidade de *deploy* de código para mudanças simples de lógica. A solução é arquitetada para ser a fundação de uma API RESTful de alto desempenho.

### 🔑 Valor Agregado (A "Dor" que Mata)

1.  **Flexibilidade (Low-Code):** Regras dinâmicas para gerentes e analistas (evitando dependência do time de TI).

2.  **Auditoria (Compliance):** Geração de log (`log_validacao`) para cada falha de regra, vital para rastreamento e *compliance*.

3.  **Escalabilidade:** Base de código desacoplada para fácil transição para o modelo Multi-Tenant.

2\. Arquitetura do Sistema
--------------------------

### 🏗️ Stack Tecnológico

| Componente | Ferramenta | Objetivo |
| --- | --- | --- |
| **Lógica Core** | Python (POO) | Regras, Validação e Abstração. |
| **Banco de Dados** | PostgreSQL | Persistência de Regras (DDL + Integridade). |
| **Containerização** | Docker Compose | Isolamento, Imutabilidade e Facilidade de *Deploy*. |
| **Conectividade** | Psycopg2 | Driver oficial para conexão Python ↔ PostgreSQL. |


### 🧭 Fluxo de Dados (Fase CLI)

1.  **`database.py`:** Gerencia a conexão, DDL, *seeding* inicial (`seed_data`) e carregamento das regras ativas (`load_rules`).

2.  **`rule_engine.py`:** Recebe a lista de regras do `database.py`.

3.  **Core Logic:** O método `RuleEngine.validate()` executa a lógica de Inversão de Controle, comparando o `valor_do_dado` (do cliente) com o `valor_esperado` (do DB) através do `operator.map`.

3\. Setup Local e Execução
--------------------------

### Pré-requisitos

-   Git

-   Docker e Docker Compose

### Build e Execução com Docker Compose

    ```
    # 1. Constrói as imagens e inicia os containers
    docker compose up --build

    # Se quiser rodar em background (modo detached) para parar o log de pi_user:
    # docker compose up -d

    # 2. Verifica os logs da aplicação Python (rule_engine_app)
    docker compose logs -f rule_engine_app
    ```

-   A aplicação Python será executada, se conectará ao DB, populará as regras e executará o teste de validação do bloco `if __name__ == "__main__":`.

4\. Estrutura do Código e PI Essencial
--------------------------------------

### 📂 Estrutura de Diretórios

```
saas_rule_engine/
├── .env          # Variáveis de ambiente (IGNORADO)
├── .gitignore    # Regras de exclusão
├── docker-compose.yml
├── Dockerfile
└── rule-engine/
    ├── __init__.py
    ├── database.py   # Gerenciamento de DB e DDL
    └── rule_engine.py # CLASSE CORE (Propriedade Intelectual)

```

### 🧠 Core da Propriedade Intelectual (PI) - `rule_engine.py`

O coração do Micro-SaaS reside na classe `RuleEngine` e na sua implementação de **Inversão de Controle**:

-   **Técnica:** Mapeamento dinâmico de strings de operador (ex: `>`) para funções nativas Python (via `import operator`) dentro de um dicionário **`OPERATOR_MAP`**.

-   **Vantagem:** Evita um código poluído de `if/elif/else` e torna o motor ilimitadamente extensível a novos operadores, mantendo o método `validate()` limpo.

5\. Próximos Passos (Roadmap)
-----------------------------

A Fase 2 se concentrará na transição da CLI para a web:

1.  **Início do Módulo 4 (Django Básico):** Configurar o projeto Django para se conectar ao PostgreSQL existente.

2.  **Mapeamento de Modelos:** Usar o ORM do Django para se conectar às tabelas `regra` e `log_validacao` (criadas no `database.py`).

3.  **Desenvolvimento da API (Módulo 6):** Criar os *endpoints* **`POST /api/validate/`** e os *endpoints* **CRUD** (para gerenciar regras no DB).