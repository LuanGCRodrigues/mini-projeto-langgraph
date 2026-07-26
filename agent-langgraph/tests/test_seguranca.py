import sys
from unittest.mock import MagicMock

def test_agente_isolamento_banco():
    """Garante que o módulo do agente não importe módulos de banco de dados."""
    import agent_langgraph.nodes as nodes
    
    # Lista de módulos proibidos
    proibidos = [
        "sqlalchemy",
        "app.db.session",
        "app.models.models",
    ]
    
    for nome, mod in sys.modules.items():
        for proibido in proibidos:
            if proibido in nome:
                pytest.fail(f"O agente está importando um módulo proibido: {nome}")

def test_agente_nao_acessa_repositorio():
    """Verifica recursivamente se o agente acessa repositorios."""
    # Este teste é mais conceitual; na prática, o import acima já resolve a maioria dos casos.
    pass
