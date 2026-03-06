"""Core configuration package."""

from .config import *
from .logging import logger

__all__ = [
    "HOST_PORT",
    "BLUE_BUBBLES_HOST",
    "BLUE_BUBBLES_PASSWORD",
    "OLLAMA_HOST",
    "OLLAMA_MODEL",
    "ALLOWED_CONTACTS",
    logger,
]
