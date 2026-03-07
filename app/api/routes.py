from fastapi import APIRouter

from app.models.schemas import WebhookEvent, WebhookResponse
from app.services.agent import handle_new_message
from app.core.logging import logger

router = APIRouter()


@router.post("/webhook", response_model=WebhookResponse)
def webhook(event: WebhookEvent):
    logger.info(f"Received webhook event: {event}")
    status, detail = handle_new_message(event.data)
    return WebhookResponse(status=status, detail=detail)
