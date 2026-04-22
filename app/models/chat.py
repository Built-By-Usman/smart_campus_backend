from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import base


class ChatRoomModel(base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)  # e.g. "CS101 Group Chat"

    course_id = Column(Integer, ForeignKey("courses.id"))

    created_by = Column(Integer, ForeignKey("users.id"))


class ChatMemberModel(base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True, index=True)

    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


class MessageModel(base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))

    message = Column(String, nullable=True)  # text message

    created_at = Column(DateTime(timezone=True), server_default=func.now())
