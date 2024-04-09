# Use uma imagem base do Python
FROM python:3.8

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto para o contêiner
COPY . .

# Define a porta em que o servidor Django irá ouvir
EXPOSE 8000

# Comando para iniciar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

