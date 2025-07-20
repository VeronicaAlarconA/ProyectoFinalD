# Usa una imagen oficial ligera de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo el archivo de dependencias primero para aprovechar cache de Docker
COPY requirements.txt .

# Actualiza pip y instala dependencias sin caché para reducir tamaño
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Expone el puerto donde corre FastAPI
EXPOSE 5000

# Usa uvicorn para correr la app (más eficiente que python run.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
