"""External client wrappers (Ollama, BlueBubbles, etc.)."""

from .ollama import chat_with_ollama
from .bluebubbles import send_message

__all__ = ["chat_with_ollama", "send_message"]
