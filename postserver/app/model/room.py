from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db import Base


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    type = Column(String(60), nullable=False)
    owner = Column(String(255), nullable=False)
    price_per_day = Column(Float, nullable=False)
    owner_uuid = Column(String(255), nullable=False)
    
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, type, owner, owner_uuid, price_per_day):
        self.type = type
        self.owner = owner
        self.owner_uuid = owner_uuid
        self.price_per_day = price_per_day

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "owner": self.owner,
            "owner_uuid": self.owner_uuid,
            "price_per_day": self.price_per_day,
            
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
