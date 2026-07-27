# Mini-Projeto: Sistema de Vendas com Agente LangGraph

Este projeto implementa um sistema de análise de compras com uma separação clara entre a API de persistência (FastAPI/SQLAlchemy) e um Agente inteligente (LangGraph) que consome dados exclusivamente via HTTP.

## Arquitetura
- **`seller-system/`**: API REST que interage com o banco de dados (SQLite).
- **`agent-langgraph/`**: Agente que orquestra consultas analíticas via APIs de leitura.
- **Regra de Ouro**: O agente **NUNCA** acessa o banco de dados ou ORM. Ele atua como um cliente HTTP rigoroso.

## Funcionalidades
### APIs de Domínio & Relatórios
- Clientes, Produtos, Compras e Itens.
- Relatórios analíticos: Resumo de cliente, Produtos mais vendidos, Resumo de compras (ticket médio), Estoque baixo.

### O Agente LangGraph
- **Fluxo**: Validação -> Identificação de Intenção -> Execução (HTTP GET) -> Resposta.
- **Segurança**: Validação de parâmetros, isolamento por `session_id`, cache de contexto com TTL e sanitização de logs.

## Setup e Execução

Para rodar o projeto, você precisará de dois terminais abertos: um para a API e outro para o Agente.

### 1. Sistema de Vendas (`seller-system`)
Este serviço hospeda os dados e a lógica de persistência.
```bash
cd seller-system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
*A API estará disponível em `http://localhost:8000`*

### 2. Agente LangGraph (`agent-langgraph`)
Este serviço orquestra as consultas analíticas.
```bash
cd agent-langgraph
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Certifique-se de configurar o .env com a URL da API
python3 main.py
```
*O agente estará rodando na porta padrão do FastAPI (verificar main.py).*

### Validação (cURL)
Envie uma pergunta ao agente para validar a integração:
```bash
curl -X POST "http://localhost:8000/api/v1/agente/perguntas" \
     -H "Content-Type: application/json" \
     -d '{
           "pergunta": "Quais produtos estão com estoque baixo?",
           "session_id": "sessao-teste-01"
         }'
```

## Qualidade
- Cobertura total de testes com `pytest`.
- Teste de segurança que bloqueia acesso do agente ao banco (proibição de importações de módulos ORM).
- Isolamento de ambientes de teste.
