# Usar una imagen base ligera de Python
FROM python:3.9-slim

# Configuración de entorno para evitar prompts en la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias (incluyendo Git y Git LFS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && apt-get install -y git-lfs \
    && git lfs install \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Descargar los archivos grandes rastreados por Git LFS
RUN git lfs pull

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "API.fastapi_movies_api:app", "--host", "0.0.0.0", "--port", "8000"]
