import time
from typing import Dict, List, Optional
from threading import Lock

class SessionMemory:
    def __init__(self, ttl_seconds: int = 300):
        self._memory: Dict[str, Dict] = {}
        self._ttl = ttl_seconds
        self._lock = Lock()

    def get_context(self, session_id: str) -> Optional[str]:
        with self._lock:
            if session_id in self._memory:
                if time.time() - self._memory[session_id]["timestamp"] < self._ttl:
                    return self._memory[session_id]["context"]
                del self._memory[session_id]
        return None

    def save_context(self, session_id: str, context: str):
        with self._lock:
            self._memory[session_id] = {
                "context": context,
                "timestamp": time.time()
            }

    def cleanup(self):
        with self._lock:
            now = time.time()
            expired = [sid for sid, data in self._memory.items() if now - data["timestamp"] > self._ttl]
            for sid in expired:
                del self._memory[sid]

# Singleton instance
memory = SessionMemory()
