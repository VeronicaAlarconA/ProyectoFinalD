# Usa Python como base
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia requirements y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "run.py"]
