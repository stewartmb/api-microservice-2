# Usar una imagen ligera de Python
FROM python:3-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /home/ubuntu/api-microservice-2

# Instalar dependencias de FastAPI y MySQL
RUN pip3 install "fastapi[standard]"
RUN pip3 install pydantic
RUN pip3 install mysql-connector-python
# Instalar boto3 si lo necesitas para subir archivos a S3
RUN pip3 install boto3  

# Copiar todo el contenido del repositorio clonado al directorio de trabajo del contenedor
COPY . .

# Comando para correr FastAPI con Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]
