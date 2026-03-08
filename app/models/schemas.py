from typing import Any, List, Optional
from pydantic import BaseModel


class Chat(BaseModel):
    originalROWID: int
    guid: str
    style: int
    chatIdentifier: str
    isArchived: bool
    displayName: str


class Handle(BaseModel):
    originalROWID: int
    address: str
    service: str
    uncanonicalizedId: Optional[str]
    country: str


class NewMessageData(BaseModel):
    originalROWID: int
    guid: str
    text: str
    attributedBody: Optional[str]
    handle: Optional[Handle] = None
    handleId: int
    otherHandle: int
    attachments: List[dict]
    subject: Optional[str]
    error: int
    dateCreated: int
    dateRead: Optional[int]
    dateDelivered: Optional[int]
    isDelivered: bool
    isFromMe: bool
    hasDdResults: bool
    isArchived: bool
    itemType: int
    groupTitle: Optional[str]
    groupActionType: int
    balloonBundleId: Optional[str]
    associatedMessageGuid: Optional[str]
    associatedMessageType: Optional[int]
    expressiveSendStyleId: Optional[str]
    threadOriginatorGuid: Optional[str]
    hasPayloadData: bool
    chats: List[Chat]
    messageSummaryInfo: Optional[dict]
    payloadData: Optional[bytes]
    dateEdited: Optional[int]
    dateRetracted: Optional[int]
    partCount: int


class WebhookEvent(BaseModel):
    type: str
    data: NewMessageData


class WebhookResponse(BaseModel):
    status: str
    detail: Optional[str] = None
