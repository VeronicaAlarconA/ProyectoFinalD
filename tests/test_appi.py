import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

client = TestClient(app)

def test_add_client():
    response = client.post("/clients", json={"name": "Cliente Test"})
    assert response.status_code == 200
    data = response.json()
    assert "client_id" in data
    assert data["message"] == "Client added"

def test_add_product():
    response = client.post("/products", json={"name": "Producto Test", "price": 19.99})
    assert response.status_code == 200
    data = response.json()
    assert "product_id" in data
    assert data["message"] == "Product added"

def test_add_sale_success():
    # Primero crea un cliente
    client_resp = client.post("/clients", json={"name": "Cliente Venta"})
    client_id = client_resp.json()["client_id"]

    # Luego crea un producto
    product_resp = client.post("/products", json={"name": "Producto Venta", "price": 10.0})
    product_id = product_resp.json()["product_id"]

    # Ahora registra una venta válida
    sale_resp = client.post("/sales", json={
        "client_id": client_id,
        "product_id": product_id,
        "quantity": 3
    })
    assert sale_resp.status_code == 200
    data = sale_resp.json()
    assert data["message"] == "Sale recorded"

def test_add_sale_invalid_client_or_product():
    # Intenta crear venta con IDs inválidos
    sale_resp = client.post("/sales", json={
        "client_id": "invalid-client-id",
        "product_id": "invalid-product-id",
        "quantity": 1
    })
    assert sale_resp.status_code == 400
    data = sale_resp.json()
    assert data["detail"] == "Invalid client or product ID"
