import os  # Necessário para ler variaveis de ambiente

import psycopg2

from .rule_engine import RuleEngine


class DatabaseManager:

    def __init__(self):
        # A. Armazene a conexão e o cursor como atributos de instância.
        self.connection = None
        self.cursor = None

    def connect(self):
        # DICA 1: Como ler a 'DATABASE_URL' do sistema?
        # Use o módulo 'os' para obter o valor. O Docker já o injetou no ambiente.
        database_url = os.environ.get("DATABASE_URL")

        if not database_url:
            print("ERRO: Variável DATABASE_URL não encontrada.")
            return

        # DICA 2: Use try/except/finally (Módulo 2.5) para tentar a conexão.
        try:
            # Conecte-se usando psycopg2.connect() com a URL.
            # Se a conexão for bem-sucedida, atribua-a a self.conn
            # E crie o self.cursor a partir de self.conn.cursor()
            self.connection = psycopg2.connect(database_url)
            self.cursor = self.connection.cursor()
            print("Conexão estabelecida com sucesso.")

        except Exception as e:
            # Imprima uma mensagem clara de erro de conexão.
            print(f"ERRO DE CONEXÃO: {e}")

    def create_tables(self):
        # DICA 3: Se houver conexão, comece um bloco try/except/finally
        if not self.connection:
            print("Não é possível criar tabelas: sem conexão.")
            return

        try:
            sql_extensao_uuid = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
            self.cursor.execute(sql_extensao_uuid)
            sql_tabela_regra = """
                CREATE TABLE IF NOT EXISTS regra (
                    id_regra UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    nome_regra VARCHAR(255) NOT NULL UNIQUE,
                    campo_alvo VARCHAR(100) NOT NULL,
                    operador VARCHAR(10) NOT NULL,
                    valor_esperado VARCHAR(255),
                    mensagem_erro VARCHAR(500)
                );
            """

            sql_extensao_uuid = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
            self.cursor.execute(sql_extensao_uuid)
            sql_tabela_log_validacao = """
                CREATE TABLE IF NOT EXISTS log_validacao (
                    id_log SERIAL PRIMARY KEY,
                    id_regra UUID NOT NULL,  -- Chave Estrangeira (FK)
                    timestamp_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    registro_invalido TEXT,
                    
                    -- Define o relacionamento
                    FOREIGN KEY (id_regra) REFERENCES regra (id_regra)
                );
            """
            # 1. Defina seus comandos SQL DDL (CREATE TABLE) em variaveis de string.
            # DICA 4: Use a sintaxe SQL "CREATE TABLE IF NOT EXISTS tabela ( ... )"
            # As tabelas devem ser 'regra' e 'log_validacao' (Módulo 3.3.1).

            # 2. Execute os comandos usando self.cursor.execute(sql_string)
            self.cursor.execute(sql_tabela_regra)
            self.cursor.execute(sql_tabela_log_validacao)

            self.connection.commit()
            print("Tabelas criadas com sucesso.")
            print(sql_tabela_regra)
            print(sql_tabela_log_validacao)

            # DICA 5: Para persistir a mudança no banco (DDL), o que você deve chamar em self.connection? (Módulo 3.9)

        except psycopg2.Error as e:
            # DICA 6: Use o rollback se a transação falhar. (Módulo 3.9)
            print(f"Erro ao criar tabelas: {e}")
            self.connection.rollback()

    def close(self):
        """Fecha o cursor e a conexão."""
        if self.cursor:
            # Dica: Use um try/except aqui também, para ser robusto
            self.cursor.close()

        if self.connection:
            self.connection.close()
            print("Conexão com PostgreSQL encerrada.")

    def seed_data(self):
        """Insere dados iniciais para testes (CRUD - CREATE)."""
        if not self.connection:
            print("Erro: Sem conexão para inserir dados.")
            return

        try:
            sql = """
                    INSERT INTO regra 
                        (nome_regra, 
                        campo_alvo, 
                        operador, 
                        valor_esperado, 
                        mensagem_erro) 
                    VALUES 
                        (%s, %s, %s, %s, %s) 
                    ON CONFLICT (nome_regra) DO NOTHING;
                    """
            # A regra de exemplo que usaremos:
            data = (
                "Regra Idade Minima",
                "idade",
                ">=",
                "18",
                "Cliente deve ser maior de idade.",
            )

            self.cursor.execute(sql, data)

            self.connection.commit()
            print("Dados iniciais inseridos (ou já existiam).")

        except psycopg2.Error as e:
            print(f"Erro ao inserir dados: {e}")
            self.connection.rollback()

    def load_rules(self):
        """Carrega todas as regras de validação do banco de dados (DQL)."""
        if not self.connection:
            print("Erro: Não há conexão para carregar regras.")

        try:
            sql = """ 
                    SELECT
                        id_regra,
                        nome_regra,
                        campo_alvo,
                        operador,
                        valor_esperado,
                        mensagem_erro
                    FROM regra;
                    """
            self.cursor.execute(sql)

            # Como obter todos os resultados?
            # DICA: Pesquise a função do cursor para obter todos os resultados.
            rules = self.cursor.fetchall()
            return rules

        except psycopg2.Error as e:
            print(f"Erro ao carregar regras: {e}")
            return []


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_tables()
    db_manager.seed_data()

    rules = db_manager.load_rules()

    # 1. Cria a instância do motor de regras com as regras carregadas
    engine = RuleEngine(rules)

    # 2. Simula os dados do cliente (idade 16 deve falhar na regra ">= 18")
    dados_do_cliente = {
        "idade": 16.0,
        "valor_compra": 50.0,  # Valor não relevante, mas mantido
    }

    # 3. Executa a validação
    validation_errors = engine.validate(dados_do_cliente)

    # 4. Imprime o resultado final
    print("\n--- Resultado da Validação ---")
    if validation_errors:
        print("FALHA NA VALIDAÇÃO!")
        for error in validation_errors:
            print(f" - ERRO: {error}")
    else:
        print("SUCESSO! Nenhum erro de regra encontrado.")

    db_manager.close()
