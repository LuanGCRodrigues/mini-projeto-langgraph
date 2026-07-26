from state import AgenteState
from tools import chamar_ferramenta_http

def validar_pergunta(state: AgenteState):
    print("Validando pergunta...")
    # Lógica de validação básica
    if not state.get("pergunta_original"):
        return {"erros": ["Pergunta vazia"]}
    return {"parametros": {}}

def identificar_intencao(state: AgenteState):
    print("Identificando intenção...")
    q = state["pergunta_original"].lower()
    if "estoque" in q:
        return {"intencao": "estoque_baixo"}
    elif "resumo" in q or "compras" in q:
        return {"intencao": "resumo_compras"}
    return {"intencao": "desconhecida"}

async def executar_ferramenta(state: AgenteState):
    intencao = state.get("intencao")
    if intencao == "estoque_baixo":
        res = await chamar_ferramenta_http("/api/v1/relatorios/estoque-baixo")
        return {"resultado_ferramenta": res}
    return {"resultado_ferramenta": {"status": "error", "message": "Intenção não mapeada"}}

def gerar_resposta(state: AgenteState):
    res = state.get("resultado_ferramenta", {})
    if res.get("status") == "success":
        return {"resposta_final": f"Dados encontrados: {res['data']}"}
    return {"resposta_final": "Não foi possível completar a consulta."}
