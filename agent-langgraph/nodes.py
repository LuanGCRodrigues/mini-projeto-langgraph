from state import AgenteState
from tools import chamar_ferramenta_http
from memory import memory
import re

def validar_pergunta(state: AgenteState):
    print("Validando pergunta...")
    q = state.get("pergunta_original", "")
    if not q or len(q) > 500:
        return {"erros": ["Pergunta inválida ou muito longa"]}
    
    sid = state.get("session_id")
    if sid and not re.match(r"^[a-zA-Z0-9_-]{8,32}$", sid):
        return {"erros": ["Session ID inválido"]}

    # Recupera contexto da memória
    if sid:
        contexto = memory.get_context(sid)
        if contexto:
            return {"contexto": contexto, "parametros": {}}
    
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
    sid = state.get("session_id")
    
    if res.get("status") == "success":
        resposta = f"Dados encontrados: {res['data']}"
        if sid:
            memory.save_context(sid, resposta)
        return {"resposta_final": resposta}
    
    return {"resposta_final": "Não foi possível processar sua solicitação."}
