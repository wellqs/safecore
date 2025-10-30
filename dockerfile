# Usar uma imagem oficial e leve do Python como base
FROM python:3.11-slim

# Definir variáveis de ambiente para boas práticas
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar e instalar as dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto para o diretório de trabalho
COPY . .