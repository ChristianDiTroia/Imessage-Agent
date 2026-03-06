"""BlueBubbles client for interacting with BlueBubbles server API."""

import uuid
import requests
from app.core.logging import logger

from app.core.config import BLUE_BUBBLES_HOST, BLUE_BUBBLES_PASSWORD


def send_message(chat_guid: str, text: str, method: str = "apple-script") -> None:
    """Send a text message to a chat via BlueBubbles (fire-and-forget).

    Args:
        chat_guid: The chat GUID to send the message to.
        text: The message text.
        method: The delivery method (default: apple-script).
    """
    params = {"password": BLUE_BUBBLES_PASSWORD}
    data = {
        "chatGuid": chat_guid,
        "message": text,
        "tempGuid": str(uuid.uuid4()),
        "method": method,
    }

    try:
        response = requests.post(
            f"{BLUE_BUBBLES_HOST}/api/v1/message/text",
            json=data,
            params=params,
            headers={"Content-Type": "application/json"},
            timeout=3,
        )
        if response.status_code != 200:
            logger.warning(
                f"Warning: send_message returned status {response.status_code} (body: {response.text!r})"
            )
    except requests.exceptions.RequestException as exc:
        logger.error(f"Error sending message to BlueBubbles: {exc}")
