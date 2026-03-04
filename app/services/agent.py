from typing import Tuple

from app.models.schemas import NewMessageData
from app.clients.ollama import chat_with_ollama
from app.clients.bluebubbles import send_message
from app.core.config import ALLOWED_CONTACTS


def handle_new_message(data: NewMessageData) -> Tuple[str, str]:
    """Validate and handle a new message. Returns (status, detail)."""
    if not data.chats:
        return ("error", "no chats")

    text = data.text or ""
    chat_guid = data.chats[0].guid.strip()

    guid_match = chat_guid in ALLOWED_CONTACTS
    agent_prefix = text.strip().lower().startswith("/agent")
    from_me = bool(data.isFromMe)

    if (not guid_match and not from_me) or not agent_prefix:
        return ("ignored", "criteria not met")

    trimmed = text.strip()[6:].strip()
    if not trimmed:
        return ("ignored", "empty agent message")

    try:
        resp = chat_with_ollama(trimmed)
    except Exception as exc:
        return ("error", str(exc))

    send_message(chat_guid, resp)
    return ("ok", "message sent")
