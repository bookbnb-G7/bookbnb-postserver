from app.db import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class RoomPhoto(Base):

    __tablename__ = "room_photos"

    id = Column("id", Integer, primary_key=True)
    url = Column(String(200), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    firebase_id = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, url, room_id, firebase_id):
        self.url = url
        self.room_id = room_id
        self.firebase_id = firebase_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "room_id": self.room_id,
            "firebase_id": self.firebase_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def is_from(self, room_id):
        return self.room_id == room_id
