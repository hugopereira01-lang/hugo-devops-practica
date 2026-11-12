# Imagen de la API "Sistema de Gestión de Tienda" (Práctica 2) - Hugo Pereira López
# a. Imagen base ligera de Python
FROM python:3.12-slim
# No crear ficheros .pyc, ver los logs al momento y puerto por defecto
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
PORT=8000
WORKDIR /app
# b. Copiar primero las dependencias (así Docker reutiliza la caché)
COPY requirements.txt .
# c. Instalar las dependencias sin guardar la caché de pip
RUN pip install --no-cache-dir -r requirements.txt
# d. Copiar el código fuente
COPY src/ ./src/
# e. Crear un usuario sin privilegios y darle permisos sobre el código
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
&& chown -R appuser:appuser /app \
&& chmod -R 755 /app
USER appuser
WORKDIR /app/src
EXPOSE 8000
# f. Comando de inicio: Uvicorn escuchando en todas las interfaces
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
