import httpx
import os
from typing import Dict, Any, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ALLOWED_ROUTES = [
    "/api/v1/relatorios/clientes/{cliente_id}",
    "/api/v1/relatorios/produtos-mais-vendidos",
    "/api/v1/relatorios/resumo-compras",
    "/api/v1/relatorios/estoque-baixo"
]

async def chamar_ferramenta_http(rota: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    # Validação rigorosa de rota permitida
    url = f"{API_BASE_URL}{rota}"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
    except httpx.HTTPStatusError as e:
        return {"status": "error", "message": f"Erro HTTP: {e.response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
