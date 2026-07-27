# Recursos HTTP e validações

**Pré-requisitos:** FastAPI, modelos, migration e dados fictícios já existentes. Pode ser executado sem o agente.

```text
Implemente somente o aprimoramento das APIs de clientes, produtos e compras. Não implemente LangGraph, LLM ou ferramenta de agente.

Fluxo de trabalho obrigatório:
1. Atualize a branch principal local sem apagar alterações de terceiros.
2. Crie a branch `feat/recursos-api-validacoes`.
3. Faça commits semânticos e incrementais, por exemplo `feat(clientes): adiciona filtros e detalhe` e `test(api): cobre respostas de erro`.
4. Abra uma Pull Request para a branch principal, descrevendo testes e pedindo revisão. Mantenha evidências rastreáveis de contribuição individual por commits ou revisão de PR.

Use schemas Pydantic separados dos modelos SQLAlchemy. Implemente:
- GET /api/v1/clientes/{cliente_id};
- GET /api/v1/produtos/{produto_id};
- GET /api/v1/compras/{compra_id}, incluindo cliente e itens;
- filtros: clientes por cidade e estado; produtos por categoria e ativo; compras por cliente_id, status e intervalo de datas.

Retorne 404 para recursos inexistentes. Valide parâmetros, responda erros HTTP estruturados em português, não exponha detalhes internos do banco e feche corretamente a sessão do banco.

Os endpoints devem continuar consultando o banco; não substitua dados por listas em memória. Adicione testes para detalhes, filtros, paginação, 404 e parâmetros inválidos. Atualize o README com exemplos de chamadas e respostas.

Antes da Pull Request, execute os testes. Na resposta final, apresente arquivos alterados, comandos, resultados, branch e sugestão de PR. Não faça mudanças fora deste escopo.
```
