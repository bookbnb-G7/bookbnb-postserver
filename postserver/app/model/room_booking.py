from app.db import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, Date, Float, Integer


class RoomBooking(Base):

    __tablename__ = "room_bookings"

    id = Column(Integer, primary_key=True, autoincrement=False)
    room_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    date_ends = Column(Date, nullable=False)
    date_begins = Column(Date, nullable=False)
    amount_of_people = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, id, room_id, user_id, date_begins, date_ends, total_price, amount_of_people, status):
        self.id = id
        self.room_id = room_id
        self.user_id = user_id
        self.date_ends = date_ends
        self.date_begins = date_begins
        self.total_price = total_price
        self.amount_of_people = amount_of_people
        self.status = status

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "user_id": self.user_id,
            "date_ends": self.date_ends,
            "date_begins": self.date_begins,
            "total_price": self.total_price,
            "amount_of_people": self.amount_of_people,
            "status": self.status,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def is_from(self, room_id):
        return self.room_id == room_id
