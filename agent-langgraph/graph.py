from langgraph.graph import StateGraph, END
from state import AgenteState
from nodes import validar_pergunta, identificar_intencao, executar_ferramenta, gerar_resposta

# Construindo o grafo
workflow = StateGraph(AgenteState)

workflow.add_node("validar", validar_pergunta)
workflow.add_node("identificar", identificar_intencao)
workflow.add_node("executar", executar_ferramenta)
workflow.add_node("responder", gerar_resposta)

workflow.set_entry_point("validar")
workflow.add_edge("validar", "identificar")
workflow.add_edge("identificar", "executar")
workflow.add_edge("executar", "responder")
workflow.add_edge("responder", END)

app = workflow.compile()
