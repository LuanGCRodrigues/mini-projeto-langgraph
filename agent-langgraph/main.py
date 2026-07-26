from fastapi import FastAPI
from state import PerguntaInput, AgenteState
from graph import app

api = FastAPI()

@api.post("/api/v1/agente/perguntas")
async def processar_pergunta(input: PerguntaInput):
    state: AgenteState = {
        "pergunta_original": input.pergunta,
        "session_id": input.session_id,
        "contexto": "",
        "intencao": None,
        "parametros": {},
        "resultado_ferramenta": None,
        "resposta_final": None,
        "erros": []
    }
    
    result = await app.ainvoke(state)
    
    return {
        "session_id": result.get("session_id"),
        "intencao": result.get("intencao"),
        "dados_consultados": result.get("resultado_ferramenta"),
        "resposta": result.get("resposta_final"),
        "avisos": result.get("erros")
    }
