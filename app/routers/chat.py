from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.db.database import session_local, get_db
from app.models.chat import MessageModel
from app.schemas.chat import MessageCreate
from app.services.connection_manager import manager
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat", tags=["Chat"])


from app.schemas.chat import MessageCreate


@router.post("/")
def send_message(request: MessageCreate, db: Session = Depends(get_db)):

    new_msg = MessageModel(
        chat_room_id=request.chat_room_id,
        sender_id=request.sender_id,
        message=request.message,
    )

    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    return new_msg


@router.get("/{room_id}")
def get_messages(room_id: int, db: Session = Depends(get_db)):

    return (
        db.query(MessageModel)
        .filter(MessageModel.chat_room_id == room_id)
        .order_by(MessageModel.created_at.asc())
        .all()
    )


@router.websocket("/ws/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: int):

    db = session_local()  # ✅ manual session

    await manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            sender_id = data["sender_id"]
            message_text = data["message"]

            # -------------------
            # SAVE TO DATABASE
            # -------------------
            new_msg = MessageModel(
                chat_room_id=room_id, sender_id=sender_id, message=message_text
            )

            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)

            # -------------------
            # BROADCAST
            # -------------------
            await manager.broadcast(
                room_id,
                {
                    "id": new_msg.id,
                    "room_id": room_id,
                    "sender_id": sender_id,
                    "message": message_text,
                    "created_at": str(new_msg.created_at),
                },
            )

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

    finally:
        db.close()  # ✅ VERY IMPORTANT
