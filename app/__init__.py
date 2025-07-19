from fastapi import FastAPI
from .routes import router as main_router
from .metrics import setup_metrics

# Instancia de FastAPI con metadatos
app = FastAPI(
    title="Store API",
    description="API para gestionar clientes, productos y ventas",
    version="1.0.0"
)

# Incluye las rutas de clientes, productos y ventas
app.include_router(main_router)

# Configura Prometheus Metrics
setup_metrics(app)
