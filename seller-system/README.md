# Seller System API

API Python para análise de compras, construída com FastAPI, SQLAlchemy 2.x e Alembic.

## Requisitos

- Python 3.11+
- pip

## Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd seller-system
```

2. Crie um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Migration e Seed Data

Execute a migration inicial para criar as tabelas e inserir dados fictícios:

```bash
source .venv/bin/activate
alembic upgrade head
```

Isso criará um arquivo `app.db` com:
- 10 clientes
- 15 produtos
- 20 compras com itens relacionados
- Dados totalmente determinísticos e com integridade referencial

## Execução

Para iniciar o servidor:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Endpoints da API

### Clientes

#### Listar clientes
```
GET /api/v1/clientes?limit=10&offset=0&cidade=&estado=
```

**Parâmetros de query:**
- `limit` (int, 1-100, padrão: 10)
- `offset` (int, ≥0, padrão: 0)
- `cidade` (string, opcional) - Filtro by substring
- `estado` (string, opcional) - Filtro by substring

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/clientes?limit=5&cidade=São%20Paulo"
```

**Resposta (200):**
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com",
    "cidade": "São Paulo",
    "estado": "SP",
    "criado_em": "2026-07-20T10:30:00"
  }
]
```

#### Obter detalhe de cliente
```
GET /api/v1/clientes/{cliente_id}
```

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/clientes/1"
```

**Resposta (200):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "cidade": "São Paulo",
  "estado": "SP",
  "criado_em": "2026-07-20T10:30:00"
}
```

**Resposta (404):**
```json
{
  "detail": "Cliente com ID 999 não encontrado"
}
```

### Produtos

#### Listar produtos
```
GET /api/v1/produtos?limit=10&offset=0&categoria=&ativo=
```

**Parâmetros de query:**
- `limit` (int, 1-100, padrão: 10)
- `offset` (int, ≥0, padrão: 0)
- `categoria` (string, opcional) - Filtro by substring
- `ativo` (boolean, opcional) - Filtro por status (true/false)

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/produtos?categoria=Eletrônicos&ativo=true"
```

**Resposta (200):**
```json
[
  {
    "id": 1,
    "nome": "Notebook",
    "categoria": "Eletrônicos",
    "preco_unitario": 2500.00,
    "estoque": 10,
    "ativo": true,
    "criado_em": "2026-07-20T10:30:00"
  }
]
```

#### Obter detalhe de produto
```
GET /api/v1/produtos/{produto_id}
```

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/produtos/1"
```

**Resposta (200):**
```json
{
  "id": 1,
  "nome": "Notebook",
  "categoria": "Eletrônicos",
  "preco_unitario": 2500.00,
  "estoque": 10,
  "ativo": true,
  "criado_em": "2026-07-20T10:30:00"
}
```

**Resposta (404):**
```json
{
  "detail": "Produto com ID 999 não encontrado"
}
```

### Compras

#### Listar compras
```
GET /api/v1/compras?limit=10&offset=0&cliente_id=&status=&data_inicio=&data_fim=
```

**Parâmetros de query:**
- `limit` (int, 1-100, padrão: 10)
- `offset` (int, ≥0, padrão: 0)
- `cliente_id` (int, opcional) - Filtro por ID do cliente
- `status` (string, opcional) - Filtro by substring (pendente, confirmada, enviada, entregue, cancelada)
- `data_inicio` (datetime, opcional) - Filtro: compras criadas a partir desta data (ISO 8601)
- `data_fim` (datetime, opcional) - Filtro: compras criadas até esta data (ISO 8601)

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/compras?cliente_id=1&status=pendente"
```

**Resposta (200):**
```json
[
  {
    "id": 1,
    "cliente_id": 1,
    "criada_em": "2026-07-20T10:30:00",
    "status": "pendente",
    "valor_total": 2500.00,
    "itens": []
  }
]
```

#### Obter detalhe de compra (com cliente e produtos)
```
GET /api/v1/compras/{compra_id}
```

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/compras/1"
```

**Resposta (200):**
```json
{
  "id": 1,
  "cliente_id": 1,
  "criada_em": "2026-07-20T10:30:00",
  "status": "pendente",
  "valor_total": 2500.00,
  "cliente": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com",
    "cidade": "São Paulo",
    "estado": "SP",
    "criado_em": "2026-07-20T10:30:00"
  },
  "itens": [
    {
      "id": 1,
      "quantidade": 1,
      "preco_unitario": 2500.00,
      "subtotal": 2500.00,
      "produto": {
        "id": 1,
        "nome": "Notebook",
        "categoria": "Eletrônicos",
        "preco_unitario": 2500.00,
        "estoque": 10,
        "ativo": true,
        "criado_em": "2026-07-20T10:30:00"
      }
    }
  ]
}
```
**Resposta (404):**
```json
{
  "detail": "Compra com ID 999 não encontrada"
}
```

### Relatórios

Endpoints especializados para análise de dados e suporte a agentes inteligentes.

#### Resumo de Cliente
```
GET /api/v1/relatorios/clientes/{cliente_id}
```
Retorna dados cadastrais, total de compras, valor total gasto, data da última compra e top 5 produtos mais comprados.

#### Produtos Mais Vendidos
```
GET /api/v1/relatorios/produtos-mais-vendidos?limit=10&data_inicio=&data_fim=
```
**Parâmetros:** `limit` (1-50), `data_inicio`, `data_fim`.

#### Resumo de Compras
```
GET /api/v1/relatorios/resumo-compras?data_inicio=&data_fim=
```
Retorna quantidade total de compras, receita total e ticket médio no período.

#### Estoque Baixo
```
GET /api/v1/relatorios/estoque-baixo?limite_estoque=5
```
Retorna produtos ativos com estoque menor ou igual ao limite (mínimo 0).

## Testes

#### Filtro por intervalo de datas
```bash
# Compras dos últimos 7 dias
curl "http://localhost:8000/api/v1/compras?data_inicio=2026-07-19T00:00:00&data_fim=2026-07-26T23:59:59"
```

## Testes

Execute os testes com pytest:

```bash
source .venv/bin/activate
pytest app/tests/test_api.py -v
```

Os testes cobrem:
- **Endpoints de detalhe:** cliente, produto e compra com relacionamentos
- **Filtros:** cidade, estado, categoria, ativo, cliente_id, status, intervalo de datas
- **Paginação:** limit, offset, validação de valores
- **Erros HTTP:** 404 para recursos inexistentes, mensagens em português
- **Validação de parâmetros:** IDs não numéricos retornam 422
- **Ordenação:** clientes por ID, produtos por ID, compras por data (descendente)
- **Segurança:** erro HTTP não expõe detalhes internos do banco

**Total: 28 testes, 100% passing**

## Estrutura do Projeto

```
seller-system/
├── app/
│   ├── config/
│   │   └── settings.py       # Configurações
│   ├── db/
│   │   └── session.py         # Sessão SQLAlchemy
│   ├── models/
│   │   └── models.py          # Modelos ORM
│   ├── schemas/
│   │   └── schemas.py         # Schemas Pydantic (Base, Response, Detail)
│   ├── routes/
│   │   └── api.py             # Rotas da API
│   ├── tests/
│   │   └── test_api.py        # Testes
│   └── main.py                # Aplicação FastAPI
├── alembic/
│   ├── env.py                 # Configuração Alembic
│   ├── versions/
│   │   └── 001_initial.py     # Migration inicial
│   └── script.py.mako
├── alembic.ini                # Configuração Alembic
├── requirements.txt           # Dependências
├── .gitignore
└── README.md
```

## Modelos de Dados

### Cliente
- `id` (int, PK)
- `nome` (str, 255)
- `email` (str, 255, unique)
- `cidade` (str, 100)
- `estado` (str, 2)
- `criado_em` (datetime)

### Produto
- `id` (int, PK)
- `nome` (str, 255)
- `categoria` (str, 100)
- `preco_unitario` (float)
- `estoque` (int)
- `ativo` (bool)
- `criado_em` (datetime)

### Compra
- `id` (int, PK)
- `cliente_id` (int, FK)
- `criada_em` (datetime)
- `status` (str, 50)
- `valor_total` (float)

### ItemCompra
- `id` (int, PK)
- `compra_id` (int, FK)
- `produto_id` (int, FK)
- `quantidade` (int)
- `preco_unitario` (float)
- `subtotal` (float)

## Banco de Dados

Usa SQLite local armazenado em `app.db`. Nenhuma dependência de serviços externos.

## Desenvolvimento

- FastAPI 0.115.0
- SQLAlchemy 2.0.51
- Alembic 1.15.0
- Pydantic 2.x (incluído via FastAPI)
- Uvicorn 0.32.1
- Pytest 8.3.5

## Tratamento de Erros

Todas as respostas de erro incluem:
- **Status HTTP apropriado** (404 para não encontrado, 422 para validação inválida, etc.)
- **Mensagem de erro em português** legível
- **Sem exposição de detalhes internos** do banco de dados

Exemplo de erro de validação:
```json
{
  "detail": [
    {
      "type": "int_type",
      "loc": ["path", "cliente_id"],
      "msg": "Input should be a valid integer, unable to coerce string to int",
      "input": "abc"
    }
  ]
}
```

## Notas

- Integridade referencial garante que `valor_total` em `Compra` corresponde à soma dos subtotais de `ItemCompra`
- Dados de seed são determinísticos e regenerados a cada migration
- Ordenação estável por ID em listagens de clientes e produtos
- Compras são ordenadas por data descendente (mais recentes primeiro)
- Schemas Pydantic separados: `Base` para entrada, `Response` para listagem, `Detail` para detalhes
- Validadores customizados garantem dados válidos (preço > 0, quantidade > 0, status válido)

