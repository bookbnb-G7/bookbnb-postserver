from typing import Optional
from app.db import Session, get_db
from app.api.crud.room_dao import RoomDAO
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from app.api.models.room_model import RoomList

router = APIRouter()


@router.get("", response_model=RoomList, status_code=200)
async def get_recomended_rooms(
        db: Session = Depends(get_db),
        api_key: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    rooms_list = RoomDAO.get_recomended_rooms(db)
    amount_rooms = len(rooms_list)
    return {"amount": amount_rooms, "rooms": rooms_list}