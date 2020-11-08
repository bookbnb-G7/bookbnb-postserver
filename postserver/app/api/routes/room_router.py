from app.db import Session, get_db 
from fastapi import APIRouter, HTTPException, Depends

from app.api.crud.room_dao import RoomDAO

from app.api.models.room_model import RoomSchema, RoomPatch, RoomDB

router = APIRouter()

@router.post('/', response_model=RoomDB, status_code=201)
async def create_room(payload: RoomSchema, db: Session = Depends(get_db)):
	room_info = RoomDAO.add_new_room(db, payload)
	return room_info

@router.get('/{room_id}', response_model=RoomDB, status_code=200)
async def get_room(room_id: int,  db: Session = Depends(get_db)):
	room_info = RoomDAO.get_room(db, room_id)
	return room_info

@router.delete('/{room_id}', response_model=RoomDB, status_code=200)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
	room_info = RoomDAO.delete_room(db, room_id)
	return room_info

@router.patch('/{room_id}', response_model=RoomDB, status_code=200)
async def update_room(payload: RoomPatch, room_id: int, db: Session = Depends(get_db)):
	room_info = RoomDAO.update_room(db, room_id, payload)
	return room_info