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
1. **API**: 
   - `cd seller-system && python3 -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt && alembic upgrade head`
   - `uvicorn app.main:app --reload`
2. **Agente**:
   - `cd agent-langgraph && python3 -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
   - `python3 main.py`

## Exemplos
**Consulta de Estoque via Agente:**
`POST /api/v1/agente/perguntas`
`{ "pergunta": "Quais produtos estão com estoque baixo?", "session_id": "sessao123" }`

## Qualidade
- Cobertura total de testes com `pytest`.
- Teste de segurança que bloqueia acesso do agente ao banco (proibição de importações de módulos ORM).
- Isolamento de ambientes de teste.
