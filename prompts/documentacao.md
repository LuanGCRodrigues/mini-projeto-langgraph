# Documentação, evidências e entrega

**Pré-requisitos:** funcionalidades desejadas já disponíveis. Use este prompt para preparar a entrega, sem alterar comportamento de negócio.

```text
Finalize somente a documentação e as evidências de entrega do mini-projeto. Não mude regras de negócio, banco ou o comportamento do agente. Preserve a arquitetura: APIs consultam o banco; o agente LangGraph consome exclusivamente APIs HTTP de leitura.

Fluxo de trabalho obrigatório:
1. Atualize a branch principal local de forma segura.
2. Crie a branch `docs/entrega-mini-projeto`.
3. Faça commits semânticos, por exemplo `docs(readme): documenta fluxo do agente` e `docs(prompts): registra etapas de desenvolvimento`.
4. Abra Pull Request, solicite revisão e registre contribuições individuais por commits, documentação ou revisão de código. Não faça commit diretamente na branch principal.

Atualize README.md com:
- problema resolvido e objetivo do agente;
- arquitetura e fluxo LangGraph;
- entidades clientes, produtos, compras e itens;
- migrations, dados fictícios, configuração e execução;
- endpoints de domínio e relatórios;
- rotas HTTP consumidas pelo agente e limites da ferramenta;
- exemplos completos de requisições e respostas;
- testes, principais decisões e limitações.

Crie ou atualize `docs/prompts.md` com os prompts relevantes usados no planejamento, API, banco, agente, validação, testes e documentação. Não inclua segredos.

Adicione um checklist de entrega no README confirmando: código LangGraph com estado, nós e conexões; ferramenta HTTP real; contexto ou memória; validações; README completo; prompts em Markdown; migrations e dados fictícios; testes; `.gitignore` e ausência de credenciais.

Inclua também o checklist de submissão: repositório acessível; link revisado antes de enviar ao AVA; apresentação de até 2 slides com problema, agente, entrada, saída, ferramenta e fluxo; submissão conforme orientação do professor; não modificar o repositório após a entrega até receber a nota.

Execute os comandos de verificação documentados. Na resposta final, informe arquivos alterados, comandos, resultados, branch, título/descrição da PR e itens que o aluno ainda deve executar manualmente no AVA. Não envie nada ao AVA e não faça alterações fora da documentação.
```
