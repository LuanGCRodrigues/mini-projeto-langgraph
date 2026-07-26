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


def test_list_clientes_filtro_cidade(client):
    """Test listing clientes filtered by cidade"""
    response = client.get("/api/v1/clientes?cidade=São Paulo")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for cliente in data:
        if 'cidade' in cliente and cliente['cidade']:
            assert 'São Paulo' in cliente['cidade']


def test_list_clientes_filtro_estado(client):
    """Test listing clientes filtered by estado"""
    response = client.get("/api/v1/clientes?estado=SP")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for cliente in data:
        if 'estado' in cliente and cliente['estado']:
            assert cliente['estado'] == 'SP'


def test_get_cliente_detalhe(client):
    """Test getting cliente details"""
    response = client.get("/api/v1/clientes")
    assert response.status_code == 200
    clientes = response.json()
    if len(clientes) > 0:
        cliente_id = clientes[0]['id']
        response = client.get(f"/api/v1/clientes/{cliente_id}")
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == cliente_id
        assert 'nome' in data
        assert 'email' in data
        assert 'criado_em' in data


def test_get_cliente_nao_encontrado(client):
    """Test 404 for non-existent cliente"""
    response = client.get("/api/v1/clientes/99999")
    assert response.status_code == 404
    assert 'detail' in response.json()
    assert 'não encontrado' in response.json()['detail']


def test_get_cliente_id_invalido(client):
    """Test invalid cliente ID parameter"""
    response = client.get("/api/v1/clientes/abc")
    assert response.status_code == 422


def test_list_produtos(client):
    """Test listing produtos with seed data"""
    response = client.get("/api/v1/produtos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in p and 'nome' in p and 'preco_unitario' in p for p in data)


def test_list_produtos_filtro_categoria(client):
    """Test listing produtos filtered by categoria"""
    response = client.get("/api/v1/produtos?categoria=Eletrônicos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_produtos_filtro_ativo(client):
    """Test listing produtos filtered by ativo status"""
    response = client.get("/api/v1/produtos?ativo=true")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for produto in data:
        assert produto.get('ativo', True) == True


def test_get_produto_detalhe(client):
    """Test getting produto details"""
    response = client.get("/api/v1/produtos")
    assert response.status_code == 200
    produtos = response.json()
    if len(produtos) > 0:
        produto_id = produtos[0]['id']
        response = client.get(f"/api/v1/produtos/{produto_id}")
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == produto_id
        assert 'nome' in data
        assert 'preco_unitario' in data
        assert 'criado_em' in data


def test_get_produto_nao_encontrado(client):
    """Test 404 for non-existent produto"""
    response = client.get("/api/v1/produtos/99999")
    assert response.status_code == 404
    assert 'detail' in response.json()
    assert 'não encontrado' in response.json()['detail']


def test_get_produto_id_invalido(client):
    """Test invalid produto ID parameter"""
    response = client.get("/api/v1/produtos/xyz")
    assert response.status_code == 422


def test_list_compras(client):
    """Test listing compras with seed data"""
    response = client.get("/api/v1/compras")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in c and 'cliente_id' in c and 'valor_total' in c for c in data)


def test_list_compras_filtro_cliente(client):
    """Test listing compras filtered by cliente_id"""
    response = client.get("/api/v1/compras")
    assert response.status_code == 200
    compras = response.json()
    if len(compras) > 0:
        cliente_id = compras[0]['cliente_id']
        response = client.get(f"/api/v1/compras?cliente_id={cliente_id}")
        assert response.status_code == 200
        data = response.json()
        for compra in data:
            assert compra['cliente_id'] == cliente_id


def test_list_compras_filtro_status(client):
    """Test listing compras filtered by status"""
    response = client.get("/api/v1/compras?status=pendente")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_compra_detalhe(client):
    """Test getting compra details with cliente and itens"""
    response = client.get("/api/v1/compras")
    assert response.status_code == 200
    compras = response.json()
    if len(compras) > 0:
        compra_id = compras[0]['id']
        response = client.get(f"/api/v1/compras/{compra_id}")
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == compra_id
        assert 'cliente_id' in data
        assert 'status' in data
        assert 'valor_total' in data
        assert 'criada_em' in data
        assert 'cliente' in data
        assert 'itens' in data
        assert isinstance(data['itens'], list)


def test_get_compra_detalhe_inclui_cliente(client):
    """Test that compra detail includes cliente information"""
    response = client.get("/api/v1/compras")
    assert response.status_code == 200
    compras = response.json()
    if len(compras) > 0:
        compra_id = compras[0]['id']
        response = client.get(f"/api/v1/compras/{compra_id}")
        assert response.status_code == 200
        data = response.json()
        assert 'cliente' in data
        assert data['cliente'] is not None
        assert 'id' in data['cliente']
        assert 'nome' in data['cliente']
        assert 'email' in data['cliente']


def test_get_compra_detalhe_inclui_produtos(client):
    """Test that compra detail includes product information in itens"""
    response = client.get("/api/v1/compras")
    assert response.status_code == 200
    compras = response.json()
    if len(compras) > 0:
        compra_id = compras[0]['id']
        response = client.get(f"/api/v1/compras/{compra_id}")
        assert response.status_code == 200
        data = response.json()
        if len(data['itens']) > 0:
            item = data['itens'][0]
            assert 'produto' in item
            assert item['produto'] is not None
            assert 'id' in item['produto']
            assert 'nome' in item['produto']


def test_get_compra_nao_encontrada(client):
    """Test 404 for non-existent compra"""
    response = client.get("/api/v1/compras/99999")
    assert response.status_code == 404
    assert 'detail' in response.json()
    assert 'não encontrada' in response.json()['detail']


def test_get_compra_id_invalido(client):
    """Test invalid compra ID parameter"""
    response = client.get("/api/v1/compras/invalid")
    assert response.status_code == 422


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


def test_list_compras_ordered_by_criada_em(client):
    """Test that compras are ordered by criada_em (descending)"""
    response = client.get("/api/v1/compras?limit=100")
    assert response.status_code == 200
    compras = response.json()
    if len(compras) > 1:
        datas = [c['criada_em'] for c in compras]
        assert datas == sorted(datas, reverse=True)


def test_erro_nao_expoe_detalhes_internos(client):
    """Test that error responses don't expose internal details"""
    response = client.get("/api/v1/clientes/99999")
    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert 'traceback' not in data
    assert 'stack' not in data

