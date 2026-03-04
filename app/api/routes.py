from fastapi import APIRouter

from app.models.schemas import WebhookEvent, WebhookResponse
from app.services.agent import handle_new_message

router = APIRouter()


@router.post("/webhook", response_model=WebhookResponse)
def webhook(event: WebhookEvent):
    """Webhook endpoint that delegates work to service layer."""
    status, detail = handle_new_message(event.data)
    return WebhookResponse(status=status, detail=detail)
