from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db import Base


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    type = Column(String(60), nullable=False)
    owner = Column(String(255), nullable=False)
    owner_id = Column(Integer, nullable=False)
    price_per_day = Column(Float, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, type, owner, owner_id, price_per_day):
        self.type = type
        self.owner = owner
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.price_per_day = price_per_day

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "owner": self.owner,
            "owner_id": self.owner_id,
            "price_per_day": self.price_per_day,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
