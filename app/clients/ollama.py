import ollama
from typing import Optional
import os

from app.core.logging import logger
from app.core.config import OLLAMA_HOST, OLLAMA_MODEL


def _load_system_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "ollama_system_prompt.md")
    try:
        with open(prompt_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Failed to load system prompt: file not found at {prompt_path}")
        return (
            "You are a helpful AI assistant chatting with Imessage users, "
            "Keep responses concise and mobile-friendly/compatible."
        )


def _ensure_host():
    if OLLAMA_HOST:
        ollama._client.base_url = OLLAMA_HOST


def chat_with_ollama(message: str, model: Optional[str] = None) -> str:
    """Send `message` to Ollama with system prompt and return assistant text."""
    if model is None:
        model = OLLAMA_MODEL

    _ensure_host()

    system_prompt = _load_system_prompt()

    try:
        resp = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
        )
        if (
            resp
            and getattr(resp, "message", None)
            and getattr(resp.message, "content", None)
        ):
            return resp.message.content
        return str(resp)
    except Exception as e:
        logger.error(f"Ollama chat error: {e}")
        raise RuntimeError(f"Ollama chat error: {e}")
