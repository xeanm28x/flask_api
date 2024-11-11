# Dockerfile da flask_api

# Use uma imagem base do Python 3.9
FROM python:3.9

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requirements para o contêiner
COPY requirements.txt .

# Atualize o pip antes de instalar as dependências
RUN pip install --upgrade pip

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o contêiner
COPY . .

# Exponha a porta em que o Flask irá rodar (5001)
EXPOSE 5001

# Comando para iniciar a aplicação Flask
CMD ["python", "app.py"]
