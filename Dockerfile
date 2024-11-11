# Dockerfile da flask_api

# Use uma imagem base do Python 3.10
FROM python:3.10

# Instale pacotes do sistema necessários, incluindo python3-apt
RUN apt-get update && apt-get install -y \
    distro-info \
    python3-apt \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requirements e constraints para o contêiner
COPY requirements.txt .
COPY constraints.txt .

# Atualize o pip antes de instalar as dependências
RUN pip install --upgrade pip

RUN pip install Cython

# Instale as dependências do Python com as restrições
RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

# Copie o código da aplicação para o contêiner
COPY . .

# Exponha a porta em que o Flask irá rodar (5001)
EXPOSE 5001

# Comando para iniciar a aplicação Flask
CMD ["python", "app.py"]
