import sys
import os
import pytest
from fastapi.testclient import TestClient

# Asegura importar desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

client = TestClient(app)

# ---------- Pruebas de Clientes ----------
def test_add_client():
    response = client.post("/clients", json={"name": "Cliente Test"})
    assert response.status_code == 200
    data = response.json()
    assert "client_id" in data
    assert data["message"] == "Client added"

def test_list_clients():
    client.post("/clients", json={"name": "Cliente A"})
    response = client.get("/clients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- Pruebas de Productos ----------
def test_add_product():
    response = client.post("/products", json={"name": "Producto Test", "price": 19.99})
    assert response.status_code == 200
    data = response.json()
    assert "product_id" in data
    assert data["message"] == "Product added"

def test_list_products():
    client.post("/products", json={"name": "Producto A", "price": 9.99})
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- Pruebas de Ventas ----------
def test_add_sale_success():
    # Crear cliente
    client_resp = client.post("/clients", json={"name": "Cliente Venta"})
    client_id = client_resp.json()["client_id"]

    # Crear producto
    product_resp = client.post("/products", json={"name": "Producto Venta", "price": 10.0})
    product_id = product_resp.json()["product_id"]

    # Registrar venta
    sale_resp = client.post("/sales", json={
        "client_id": client_id,
        "product_id": product_id,
        "quantity": 3
    })
    assert sale_resp.status_code == 200
    data = sale_resp.json()
    assert data["message"] == "Sale recorded"

def test_add_sale_invalid_client_or_product():
    response = client.post("/sales", json={
        "client_id": "invalid-client-id",
        "product_id": "invalid-product-id",
        "quantity": 1
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid client or product ID"

def test_list_sales():
    response = client.get("/sales")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- Pruebas de Métricas ----------
def test_metrics_exposed():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.content
