# Memória, segurança e resiliência

**Pré-requisitos:** endpoint do agente e ferramenta HTTP já existentes. Este prompt não altera o banco nem as APIs de domínio.

```text
Implemente somente memória de sessão, segurança e resiliência do agente LangGraph que consome APIs HTTP. Preserve a regra: o agente não acessa diretamente o banco, ORM, SQL ou repositórios.

Fluxo de trabalho obrigatório:
1. Atualize a branch principal local de forma segura.
2. Crie a branch `feat/memoria-seguranca-agente`.
3. Use commits semânticos, por exemplo `feat(memoria): isola contexto por sessao` e `test(seguranca): bloqueia parametros invalidos`.
4. Abra Pull Request, solicite revisão e registre os testes. Em grupo, garanta evidências de contribuição individual.

Implemente memória local, limitada e testável por session_id. Ela deve permitir referência ao contexto anterior quando aplicável, nunca vazar dados entre sessões e expirar ou limpar sessões antigas.

Valide tamanho da pergunta, formato de session_id e todos os parâmetros antes da ferramenta HTTP. A ferramenta deve continuar limitada a GET e à lista fechada de rotas. Não registre pergunta completa ou dado sensível em logs de produção. Centralize configuração em variáveis de ambiente e crie `.env.example` sem valores reais.

Trate exceções inesperadas sem expor stack trace, URL interna, credenciais ou detalhes do banco nas respostas HTTP. Teste isolamento de memória, expiração, entradas inválidas, rotas não permitidas, métodos não permitidos e falhas HTTP controladas.

Atualize o README com comportamento de memória e variáveis de configuração. Execute testes antes da PR e reporte arquivos, comandos, resultados, branch e PR sugerida. Não implemente novos relatórios ou mudanças de domínio.
```
