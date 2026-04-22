from pydantic import BaseModel


class MessageCreate(BaseModel):
    chat_room_id: int
    sender_id: int
    message: str
