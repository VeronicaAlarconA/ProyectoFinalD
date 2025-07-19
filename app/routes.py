from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()

# Bases de datos en memoria
clients = {}
products = {}
sales = []

# Modelos
class ClientIn(BaseModel):
    name: str

class ClientOut(BaseModel):
    id: str
    name: str

class ProductIn(BaseModel):
    name: str
    price: float

class ProductOut(BaseModel):
    id: str
    name: str
    price: float

class SaleIn(BaseModel):
    client_id: str
    product_id: str
    quantity: int

class SaleOut(SaleIn):
    total: float

# Rutas
@router.post("/clients", response_model=ClientOut)
def add_client(client: ClientIn):
    client_id = str(uuid4())
    new_client = {"id": client_id, "name": client.name}
    clients[client_id] = new_client
    return new_client

@router.get("/clients", response_model=list[ClientOut])
def list_clients():
    return list(clients.values())

@router.post("/products", response_model=ProductOut)
def add_product(product: ProductIn):
    product_id = str(uuid4())
    new_product = {"id": product_id, "name": product.name, "price": product.price}
    products[product_id] = new_product
    return new_product

@router.get("/products", response_model=list[ProductOut])
def list_products():
    return list(products.values())

@router.post("/sales", response_model=SaleOut)
def add_sale(sale: SaleIn):
    if sale.client_id not in clients:
        raise HTTPException(status_code=400, detail="Invalid client ID")
    if sale.product_id not in products:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = products[sale.product_id]
    total = product["price"] * sale.quantity
    sale_record = sale.dict()
    sale_record["total"] = total
    sales.append(sale_record)
    return sale_record

@router.get("/sales", response_model=list[SaleOut])
def list_sales():
    return sales
