import ollama
from typing import Optional
import os

from app.core.logging import logger
from app.core.config import MODEL_CONTEXT_SIZE, OLLAMA_HOST, OLLAMA_MODEL
from app.utils.chat_context import ChatContext

_chat_context: dict[str, ChatContext] = {}  # Store context for each chat by chat guid


def _load_system_prompt() -> tuple[str, int]:
    prompt_path = os.path.join(os.path.dirname(__file__), "ollama_system_prompt.md")
    try:
        with open(prompt_path, "r") as f:
            prompt = f.read()
    except FileNotFoundError:
        logger.error(f"Failed to load system prompt: file not found at {prompt_path}")
        return (
            "You are a helpful AI assistant chatting with Imessage users, "
            "Keep responses concise and mobile-friendly/compatible."
        ), 30  # Fallback token count estimation
    try:
        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "system", "content": prompt}],
            options={"num_ctx": MODEL_CONTEXT_SIZE},
        )
        token_count = (
            resp.eval_count
            if resp and getattr(resp, "eval_count", None)
            else (prompt.count(" ") + 1) * 1.5  # Fallback token count estimation
        )
        return prompt, token_count
    except Exception as e:
        logger.error(f"Error evaluating system prompt token size with Ollama: {e}")
        return (prompt.count(" ") + 1) * 1.5  # Fallback token count estimation


(_system_prompt, _system_prompt_token_count) = _load_system_prompt()


def _ensure_host():
    if OLLAMA_HOST:
        ollama._client.base_url = OLLAMA_HOST


def chat_with_ollama(message: str, chat_guid: str) -> str:
    """Send `message` to Ollama with system prompt and return assistant text."""

    _ensure_host()

    if chat_guid not in _chat_context:
        _chat_context[chat_guid] = ChatContext(
            MODEL_CONTEXT_SIZE - _system_prompt_token_count
        )

    context = _chat_context[chat_guid]
    context.add_chat_context(message, 0)

    messages = [
        {"role": "user", "content": content} for content in context.get_chat_context()
    ]
    messages.insert(0, {"role": "system", "content": _system_prompt})

    try:
        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            options={"num_ctx": MODEL_CONTEXT_SIZE},
        )
        if (
            resp
            and getattr(resp, "message", None)
            and getattr(resp.message, "content", None)
        ):
            new_context_size = (
                resp.eval_count
                - context.get_current_context_size()
                - _system_prompt_token_count
            )
            context.add_chat_context(resp.message.content, new_context_size)
            return resp.message.content

        return str(resp)
    except Exception as e:
        logger.error(f"Ollama chat error: {e}")
        raise RuntimeError(f"Ollama chat error: {e}")
