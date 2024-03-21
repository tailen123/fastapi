from pydantic import BaseModel


class MessageBase(BaseModel):
    id: int
    dialog_id: int
    message_id: int
    is_del: bool
    text: str
    text_zh: str
    from_user: bool
    created_at: str
    reason: str
    reason_type: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    class Config:
        from_attributes = True


class Message_list(BaseModel):
    messages: list[Message]
