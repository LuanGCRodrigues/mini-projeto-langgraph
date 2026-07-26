import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_clientes(client):
    """Test listing clientes with seed data"""
    response = client.get("/api/v1/clientes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in c and 'nome' in c and 'email' in c for c in data)


def test_list_clientes_pagination(client):
    """Test pagination with limit and offset"""
    response1 = client.get("/api/v1/clientes?limit=5&offset=0")
    assert response1.status_code == 200
    assert len(response1.json()) <= 5
    
    response2 = client.get("/api/v1/clientes?limit=10&offset=5")
    assert response2.status_code == 200


def test_list_clientes_invalid_limit(client):
    """Test invalid limit parameter"""
    response = client.get("/api/v1/clientes?limit=101")
    assert response.status_code == 422


def test_list_clientes_invalid_offset(client):
    """Test invalid offset parameter"""
    response = client.get("/api/v1/clientes?offset=-1")
    assert response.status_code == 422


def test_list_produtos(client):
    """Test listing produtos with seed data"""
    response = client.get("/api/v1/produtos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in p and 'nome' in p and 'preco_unitario' in p for p in data)


def test_list_compras(client):
    """Test listing compras with seed data"""
    response = client.get("/api/v1/compras")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in c and 'cliente_id' in c and 'valor_total' in c for c in data)


def test_list_clientes_ordered(client):
    """Test that clientes are ordered by id"""
    response = client.get("/api/v1/clientes?limit=100")
    assert response.status_code == 200
    clientes = response.json()
    ids = [c['id'] for c in clientes]
    assert ids == sorted(ids)


def test_list_produtos_ordered(client):
    """Test that produtos are ordered by id"""
    response = client.get("/api/v1/produtos?limit=100")
    assert response.status_code == 200
    produtos = response.json()
    ids = [p['id'] for p in produtos]
    assert ids == sorted(ids)


def test_list_compras_ordered(client):
    """Test that compras are ordered by id"""
    response = client.get("/api/v1/compras?limit=100")
    assert response.status_code == 200
    compras = response.json()
    ids = [c['id'] for c in compras]
    assert ids == sorted(ids)
