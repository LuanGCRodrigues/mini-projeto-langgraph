import os
from typing import TypedDict, List, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

class AgenteState(TypedDict):
    pergunta_original: str
    session_id: Optional[str]
    contexto: Optional[str]
    intencao: Optional[str]
    parametros: Dict[str, Any]
    resultado_ferramenta: Optional[Dict[str, Any]]
    resposta_final: Optional[str]
    erros: List[str]

# Estrutura do endpoint de entrada
class PerguntaInput(BaseModel):
    pergunta: str
    session_id: Optional[str] = None
