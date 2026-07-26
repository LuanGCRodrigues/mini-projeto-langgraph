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

### Endpoints

- `GET /health` - Health check
- `GET /api/v1/clientes` - Lista clientes com paginação
- `GET /api/v1/produtos` - Lista produtos com paginação
- `GET /api/v1/compras` - Lista compras com paginação

### Parâmetros de Paginação

Todos os endpoints de listagem suportam:
- `limit` (int, 1-100, padrão: 10) - Número de itens por página
- `offset` (int, ≥0, padrão: 0) - Número de itens a pular

Exemplo:
```bash
curl "http://localhost:8000/api/v1/clientes?limit=20&offset=0"
```

## Testes

Execute os testes com pytest:

```bash
source .venv/bin/activate
pytest app/tests/test_api.py -v
```

Os testes cobrem:
- Health check
- Endpoints vazios (sem dados)
- Paginação (limit e offset)
- Validação de parâmetros
- Ordenação estável por ID

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
│   │   └── schemas.py         # Schemas Pydantic
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

- FastAPI 0.111.0
- SQLAlchemy 2.0.51
- Alembic 1.14.0
- Pydantic 2.x (incluído via FastAPI)
- Uvicorn 0.30.0
- Pytest 8.2.0

## Notas

- Integridade referencial garante que `valor_total` em `Compra` corresponde à soma dos subtotais de `ItemCompra`
- Dados de seed são determinísticos e regenerados a cada migration
- Ordenação estável por ID em todas as listagens
