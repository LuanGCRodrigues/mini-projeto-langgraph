# Qualidade e testes

**Pré-requisitos:** quaisquer módulos já implementados. Use este prompt para consolidar qualidade sem alterar o escopo de negócio.

```text
Revise somente qualidade, testes e confiabilidade da aplicação FastAPI e do agente LangGraph. Não adicione recursos de domínio nem permita acesso direto do agente ao banco; o agente deve continuar consumindo apenas as APIs HTTP.

Fluxo de trabalho obrigatório:
1. Atualize a branch principal local de forma segura.
2. Crie a branch `test/qualidade-integracao`.
3. Faça commits semânticos, por exemplo `test(integracao): cobre fluxo agente via API` e `chore(qualidade): configura lint`.
4. Abra Pull Request com o resultado dos testes e solicite revisão. Mantenha histórico de commits e participação rastreável em projetos em grupo.

Revise organização, tipagem e duplicação. Garanta que os testes usem banco isolado e não o arquivo SQLite local de desenvolvimento. Adicione testes de integração para: migration e dados fictícios -> endpoint de relatório -> agente fazendo requisição HTTP ao endpoint -> resposta estruturada.

Adicione cobertura para 404, filtros inválidos, pergunta vazia, session_id inválido, timeout e indisponibilidade controlada da API. Inclua um teste que falhe caso o módulo do agente importe sessão, modelo, ORM ou repositório do banco. Configure lint e formatação compatíveis com o projeto, sem alterar arquivos fora do escopo.

Confirme que `.gitignore` cobre credenciais, banco local, ambientes virtuais e caches. Execute testes e verificadores configurados; corrija somente problemas encontrados. Reporte arquivos, comandos, resultados, branch e PR sugerida.
```
