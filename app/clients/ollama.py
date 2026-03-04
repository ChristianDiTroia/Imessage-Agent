import ollama
from typing import Optional

from app.core.config import OLLAMA_HOST, OLLAMA_MODEL


def _ensure_host():
    if OLLAMA_HOST:
        ollama._client.base_url = OLLAMA_HOST


def chat_with_ollama(
    message: str, model: Optional[str] = None, timeout: int = 60
) -> str:
    """Send `message` to Ollama and return assistant text."""
    if model is None:
        model = OLLAMA_MODEL

    _ensure_host()

    try:
        resp = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
        if (
            resp
            and getattr(resp, "message", None)
            and getattr(resp.message, "content", None)
        ):
            return resp.message.content
        return str(resp)
    except Exception as e:
        raise RuntimeError(f"Ollama chat error: {e}")
