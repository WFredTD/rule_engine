import operator

# Dicionário de mapeamento para as operações
OPERATOR_MAP = {
    ">=": operator.ge,  # ge = Greater than or Equal (Maior ou Igual)
    ">": operator.gt,  # gt = Greater than (Maior que)
    "<=": operator.le,  # le = Less than or Equal (Menor ou Igual)
    "<": operator.lt,  # lt = Less than (Menor que)
    "==": operator.eq,  # eq = Equal (Igual)
    "!=": operator.ne,  # ne = Not Equal (Diferente)
}


class RuleEngine:
    """
    Classe principal responsável por receber as regras e validar um dado de entrada.
    Esta implementação usa o princípio de Inversão de Controle (IoC) para desvincular
    a lógica de negócio da execução do código.
    """
    def __init__(self, rules):
        self.rules = rules

    def validate(self, data: dict):

        erros = []

        # Itera sobre todas as regras carregadas do PostgreSQL
        for regra in self.rules:
            # Desempacotamento de Tupla por índice
            nome_regra = regra[1]
            campo_alvo = regra[2]
            operador = regra[3]
            valor_esperado = regra[4]
            mensagem_erro = regra[5]

            # O valor que precisamos checar do cliente:
            valor_do_dado = data.get(campo_alvo)

            # 1. Tratamento de Campo Ausente
            if valor_do_dado is None:
                erros.append(f"ERRO: Campo '{campo_alvo}' ausente no dado de entrada.")
                continue  # Pula para a próxima regra

            # 2. Lógica de Validação e Conversão de Tipo
            try:
                # Conversão para números para comparação (necessário para operadores > / <=)
                valor_dado_num = float(valor_do_dado)
                valor_esperado_num = float(valor_esperado)
            except ValueError:
                # Se a conversão falhar adiciona a mensagem de erro à lista
                erros.append(
                    f"ERRO DE TIPO: O valor '{valor_do_dado}' ou '{valor_esperado}' da regra '{nome_regra}' não é numérico."
                )
                # Pula o restante do loop, pois a comparação não pode ser feita
                continue

            op_func = OPERATOR_MAP.get(operador)

            if op_func is None:
                erros.append(f"ERRO: Operador '{operador}' não suportado.")
                continue

            # Executa a função mapeada (ex: operator.ge(16, 18) retorna False)
            # E usa o 'not' para checar se a regra foi VIOLADA

            if not op_func(valor_dado_num, valor_esperado_num):
                # Se a operação não for verdadeira (a regra foi violada), adiciona o erro!
                erros.append(mensagem_erro)
