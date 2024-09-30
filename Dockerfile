# Usando uma imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o conteúdo da aplicação
COPY . .

# Expor a porta onde o Streamlit será executado
EXPOSE 8501

# Comando para rodar o aplicativo
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
