# Usa uma imagem Python leve como base
FROM python:3.13-alpine

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da sua aplicação
COPY rule-engine /app/rule-engine

# Define o comando que será executado por padrão
CMD ["python", "-m", "rule_engine.database"]