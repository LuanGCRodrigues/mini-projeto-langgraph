# Relatórios expostos por API

**Pré-requisitos:** API, banco migrado e entidades de domínio existentes. Pode ser executado sem o agente.

```text
Implemente somente relatórios HTTP de leitura para a API de compras. Não implemente LangGraph, chat ou acesso de agente ao banco.

Fluxo de trabalho obrigatório:
1. Atualize a branch principal local de forma segura.
2. Crie a branch `feat/relatorios-api`.
3. Use commits semânticos, como `feat(relatorios): adiciona resumo de cliente` e `test(relatorios): cobre filtros de periodo`.
4. Abra uma Pull Request revisável, com descrição funcional, comandos de teste e evidências de participação individual quando houver grupo.

Crie consultas de negócio que leiam o banco e retornem dados serializáveis para:
- resumo de cliente: dados, quantidade de compras, valor total gasto, última compra e produtos mais comprados;
- produtos mais vendidos: produto, quantidade vendida, receita e período;
- resumo de compras por período: quantidade, receita e ticket médio;
- estoque baixo: produtos ativos abaixo de um limite validado.

Exponha somente endpoints GET:
- /api/v1/relatorios/clientes/{cliente_id};
- /api/v1/relatorios/produtos-mais-vendidos;
- /api/v1/relatorios/resumo-compras;
- /api/v1/relatorios/estoque-baixo.

Valide datas, limites e quantidade de resultados. Use agregações no banco, evite N+1 queries e nunca altere dados. Documente parâmetros padrão no README.

Estes endpoints serão a única fonte de dados do futuro agente: mantenha contratos de resposta claros, estáveis e estruturados. Crie testes de cada relatório e de parâmetros inválidos. Execute os testes antes da PR e reporte arquivos alterados, comandos, resultados, branch e PR sugerida.
```
