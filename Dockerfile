# Use a imagem base do Python
FROM python:3.8

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório atual para o diretório de trabalho dentro do contêiner
COPY . .

# Exponha a porta 8000 para o servidor web
EXPOSE 8000

# Comando padrão para iniciar a aplicação usando Gunicorn
CMD ["gunicorn", "apiTCC.wsgi:application", "0.0.0.0:8000", "--bind"]
