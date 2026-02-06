# Usar imagem oficial do Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app.py .
COPY models/ models/
COPY ml-100k/ ml-100k/

# Expor porta da API
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
