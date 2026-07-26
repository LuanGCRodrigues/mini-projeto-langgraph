import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_relatorio_cliente_sucesso():
    # Assume que o ID 1 existe devido ao seed data
    response = client.get("/api/v1/relatorios/clientes/1")
    assert response.status_code == 200
    data = response.json()
    assert "cliente" in data
    assert "total_compras" in data
    assert "valor_total_gasto" in data
    assert "produtos_mais_comprados" in data
    assert isinstance(data["produtos_mais_comprados"], list)

def test_relatorio_cliente_nao_encontrado():
    response = client.get("/api/v1/relatorios/clientes/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente 9999 não encontrado"

def test_relatorio_produtos_mais_vendidos():
    response = client.get("/api/v1/relatorios/produtos-mais-vendidos?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "produtos" in data
    assert len(data["produtos"]) <= 5
    if len(data["produtos"]) > 0:
        p = data["produtos"][0]
        assert "produto_id" in p
        assert "quantidade_vendida" in p

def test_relatorio_resumo_compras_periodo():
    # Teste com datas no futuro (deve vir vazio ou zero)
    response = client.get("/api/v1/relatorios/resumo-compras?data_inicio=2030-01-01T00:00:00")
    assert response.status_code == 200
    data = response.json()
    assert data["quantidade_total"] == 0
    assert data["receita_total"] == 0.0

def test_relatorio_estoque_baixo_validacao():
    # Teste limite negativo (deve falhar por ge=0)
    response = client.get("/api/v1/relatorios/estoque-baixo?limite_estoque=-1")
    assert response.status_code == 422

def test_relatorio_estoque_baixo_sucesso():
    response = client.get("/api/v1/relatorios/estoque-baixo?limite_estoque=100")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert data[0]["estoque_atual"] <= 100
