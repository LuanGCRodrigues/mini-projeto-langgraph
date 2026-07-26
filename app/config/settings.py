import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/app.db"
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"
