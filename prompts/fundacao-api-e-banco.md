# Fundação da API, banco e dados fictícios

**Pré-requisitos:** repositório Git inicializado. Este prompt é independente; ele não exige LangGraph nem outros prompts.

```text
Implemente somente a fundação de uma API Python para um assistente de análise de compras. Não implemente LangGraph, chat ou LLM.

Fluxo de trabalho obrigatório:
1. Atualize sua cópia local da branch principal sem sobrescrever trabalho existente.
2. Crie a branch `feat/fundacao-api-banco` a partir da branch principal.
3. Faça commits pequenos e semânticos, por exemplo `feat(api): cria estrutura inicial FastAPI` e `feat(db): adiciona migration e dados fictícios`.
4. Não faça commit diretamente na branch principal. Ao terminar, abra uma Pull Request, descreva os testes e solicite revisão. Em trabalho em grupo, registre uma contribuição rastreável de cada participante envolvido.

Crie um projeto Python 3.12 com FastAPI, SQLAlchemy 2.x, Alembic, Pydantic, Uvicorn e Pytest. Use SQLite local, sem dependência de serviços externos. Organize o código em módulos claros para configuração, banco, modelos, schemas, rotas e testes.

Modele as entidades relacionadas:
- Cliente: id, nome, email único, cidade, estado, criado_em;
- Produto: id, nome, categoria, preco_unitario, estoque, ativo, criado_em;
- Compra: id, cliente_id, criada_em, status, valor_total;
- ItemCompra: id, compra_id, produto_id, quantidade, preco_unitario, subtotal.

Crie uma migration Alembic inicial que crie as tabelas e insira dados fictícios determinísticos: no mínimo 10 clientes, 15 produtos, 20 compras e seus itens. Garanta integridade referencial e que valor_total corresponda à soma dos itens.

Crie apenas estes endpoints:
- GET /health;
- GET /api/v1/clientes;
- GET /api/v1/produtos;
- GET /api/v1/compras.

As listagens devem consultar o banco migrado, ter `limit` entre 1 e 100, `offset` maior ou igual a zero e ordenação estável por id.

Inclua README com instalação, migration e execução; `.gitignore` para .venv, __pycache__, .env e SQLite local. Crie testes básicos para health, migration/dados e listagens.

Antes da Pull Request, execute migration e testes. Na resposta final, informe arquivos alterados, comandos executados, resultado dos testes, branch e sugestão de título/descrição da PR. Não implemente nada fora deste escopo.
```
