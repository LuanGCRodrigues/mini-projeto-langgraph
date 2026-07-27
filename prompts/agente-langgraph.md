# Agente LangGraph consumidor de APIs

**Pré-requisitos:** endpoints de relatório HTTP existentes e documentados. O agente não deve importar modelos SQLAlchemy, sessão do banco, repositórios nem executar SQL.

```text
Implemente somente um agente LangGraph que consulte as APIs HTTP existentes da aplicação para responder perguntas sobre compras. O agente não pode acessar o banco de dados direta ou indiretamente por ORM, SQLAlchemy, sessão, repositório ou SQL.

Fluxo de trabalho obrigatório:
1. Atualize a branch principal local de forma segura.
2. Crie a branch `feat/agente-langgraph-api`.
3. Faça commits semânticos e pequenos, por exemplo `feat(agente): adiciona grafo de consultas HTTP` e `test(agente): cobre bloqueio de acesso ao banco`.
4. Abra uma Pull Request com diagrama textual do fluxo, testes e pedido de revisão. Em grupo, mantenha a contribuição de cada integrante rastreável por commits, documentação ou revisão de PR.

Crie um StateGraph tipado com: pergunta original, session_id, contexto, intenção, parâmetros validados, resultado da ferramenta HTTP, resposta final e erros de validação.

Crie nós separados para:
1. validar pergunta e parâmetros;
2. preparar contexto;
3. identificar intenção;
4. chamar uma ferramenta HTTP de leitura;
5. gerar resposta estruturada.

A ferramenta deve usar um cliente HTTP configurável por `API_BASE_URL` e fazer somente requisições GET para uma lista fechada de rotas:
- /api/v1/relatorios/clientes/{cliente_id};
- /api/v1/relatorios/produtos-mais-vendidos;
- /api/v1/relatorios/resumo-compras;
- /api/v1/relatorios/estoque-baixo.

Não aceite URL fornecida pelo usuário. Não permita qualquer outro método HTTP, rota, SQL, escrita, acesso a arquivos ou importação de módulos do banco. Trate timeouts, 404 e erros 5xx com respostas estruturadas, sem expor detalhes internos.

Crie POST /api/v1/agente/perguntas com `pergunta` e `session_id` opcional. A resposta deve conter session_id, intenção, dados_consultados, resposta e avisos. Mantenha a classificação de intenção determinística e isolada; não integre LLM externo nesta etapa.

Use mocks de HTTP ou um servidor de teste nos testes. Cubra cada intenção, timeout, erro HTTP, pergunta inválida e a garantia de que o pacote do agente não importa nem acessa o banco. Atualize README com fluxo, rotas consumidas, configuração API_BASE_URL e exemplos.

Execute os testes antes da PR e reporte arquivos alterados, comandos, resultados, branch e PR sugerida. Não implemente memória persistente nem outras funcionalidades.
```
