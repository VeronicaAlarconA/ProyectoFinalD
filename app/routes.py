from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()

# Bases de datos en memoria (diccionarios)
clients = {}
products = {}
sales = []

# Modelos de entrada
class ClientIn(BaseModel):
    name: str

class ProductIn(BaseModel):
    name: str
    price: float

class SaleIn(BaseModel):
    client_id: str
    product_id: str
    quantity: int

# Crear cliente
@router.post("/clients")
def add_client(client: ClientIn):
    client_id = str(uuid4())
    clients[client_id] = {"id": client_id, "name": client.name}
    return {"message": "Client added", "client_id": client_id}

# Listar clientes
@router.get("/clients")
def list_clients():
    return list(clients.values())

# Crear producto
@router.post("/products")
def add_product(product: ProductIn):
    product_id = str(uuid4())
    products[product_id] = {
        "id": product_id,
        "name": product.name,
        "price": product.price
    }
    return {"message": "Product added", "product_id": product_id}

# Listar productos
@router.get("/products")
def list_products():
    return list(products.values())

# Registrar venta
@router.post("/sales")
def add_sale(sale: SaleIn):
    if sale.client_id not in clients or sale.product_id not in products:
        raise HTTPException(status_code=400, detail="Invalid client or product ID")
    sales.append(sale.dict())
    return {"message": "Sale recorded"}

# Listar ventas
@router.get("/sales")
def list_sales():
    return sales
