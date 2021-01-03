from app.db import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, Date, Float, Integer


class RoomBooking(Base):

    __tablename__ = "room_bookings"

    id = Column(Integer, primary_key=True, autoincrement=False)
    room_id = Column(Integer, nullable=False)
    date_to = Column(Date, nullable=False)
    date_from = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, id, room_id, date_from, date_to):
        self.id = id
        self.room_id = room_id
        self.date_to = date_to
        self.date_from = date_from

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "date_to": self.date_to,
            "date_from": self.date_from,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def is_from(self, room_id):
        return self.room_id == room_id
