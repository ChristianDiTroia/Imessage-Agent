from typing import List, Optional
from pydantic import BaseModel


class Chat(BaseModel):
    guid: str


class NewMessageData(BaseModel):
    text: str
    chats: List[Chat]
    isFromMe: Optional[bool] = False


class WebhookEvent(BaseModel):
    type: str
    data: NewMessageData


class WebhookResponse(BaseModel):
    status: str
    detail: Optional[str] = None
