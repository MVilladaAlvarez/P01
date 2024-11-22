FROM python:3.9-slim

# Instalar git, git-lfs y curl
RUN apt-get update && apt-get install -y git curl \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && apt-get install -y git-lfs \
    && git lfs install

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Clonar el repositorio completo y seleccionar la rama 'master' para mantener .git y LFS
RUN git clone --branch master https://github.com/MVilladaAlvarez/P01.git /app

# Cambiar al directorio de trabajo del repositorio clonado
WORKDIR /app

# Descargar los archivos grandes con Git LFS
RUN git lfs pull

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "API.fastapi_movies_api:app", "--host", "0.0.0.0", "--port", "8000"]
