from typing import Tuple
from collections import deque
import time
import threading

from app.models.schemas import NewMessageData
from app.clients.ollama import chat_with_ollama
from app.clients.bluebubbles import send_message
from app.core.logging import logger
from app.core.config import ALLOWED_CONTACTS


def _meets_agent_trigger_criteria(data: NewMessageData) -> bool:
    """
    Check if the message meets criteria to trigger the agent.

    Criteria:
    - Message must have text.
    - Sender's address must be in ALLOWED_CONTACTS or message must be from the user's own account (isFromMe).
    - Message text must start with "/agent" (case-insensitive).
    """

    text = data.text.strip()
    if not text:
        return False

    from_me = bool(data.isFromMe)
    if data.handle:
        sender_address = data.handle.address.strip()
    else:
        # fallback for when handle isn't sent (in some group chat scenarios), use guid and strip the 'iMessage;-;' prefix if present
        sender_address = data.chats[0].guid.strip()[11:]

    address_match = sender_address in ALLOWED_CONTACTS
    agent_prefix = text.strip().lower().startswith("/agent")

    return (address_match or from_me) and agent_prefix


# Recent messages (timestamp, sender_address, text) used to suppress duplicate
# arrivals within a short window. Protect with a lock for thread-safety.
_RECENT_WINDOW = 3.0  # seconds
_recent_messages = deque()  # type: deque[tuple[float, str, str]]
_recent_messages_lock = threading.Lock()


def _prune_recent_messages(now: float | None = None) -> None:
    if now is None:
        now = time.time()
    cutoff = now - _RECENT_WINDOW
    with _recent_messages_lock:
        while _recent_messages and _recent_messages[0][0] < cutoff:
            _recent_messages.popleft()


def _is_unique_message(sender_address: str, text: str) -> bool:
    """Return True and record the (sender, text) pair if it hasn't been
    seen in the recent window. If it's a duplicate, return False.
    """
    now = time.time()
    _prune_recent_messages(now)
    with _recent_messages_lock:
        for ts, addr, t in _recent_messages:
            if addr == sender_address and t == text:
                return False
        _recent_messages.append((now, sender_address, text))
    return True


def handle_new_message(data: NewMessageData) -> Tuple[str, str]:
    """Validate and handle a new message. Returns (status, detail)."""

    sender_address = (
        data.chats[0].guid.strip()[11:]
        if data.handle is None
        else data.handle.address.strip()
    )

    if not _meets_agent_trigger_criteria(data):
        logger.info(
            f"Ignoring message {data.text} from {sender_address}: does not meet trigger criteria"
        )
        return ("ignored", "does not meet agent trigger criteria")

    chat_guid = data.chats[0].guid.strip()
    # Check uniqueness using the raw incoming text (including the "/agent" prefix)
    incoming_text = data.text.strip()
    if not _is_unique_message(sender_address, incoming_text):
        logger.info(
            f"Ignoring duplicate message from {sender_address}: {incoming_text}"
        )
        return ("ignored", "duplicate message within recent window")

    text = f"{sender_address}: {incoming_text[6:].strip()}"  # Postfix addr and remove "/agent" prefix

    try:
        logger.info(f"Sending chat message to Ollama from {sender_address}: {text}")
        resp = chat_with_ollama(text, chat_guid)
    except Exception as exc:
        logger.error(f"Error communicating with Ollama: {exc}")
        return ("error", str(exc))

    logger.info(f"Sending response from Ollama to {chat_guid}: {resp}")
    send_message(chat_guid, resp)
    return ("ok", "message sent")
