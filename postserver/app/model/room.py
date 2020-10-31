from app.db import Base 
from sqlalchemy import Column, String, Integer, Float

class Room(Base):

	__tablename__ = 'rooms'

	id = Column(Integer, primary_key=True)
	type = Column(String(60), nullable=False)
	owner = Column(String(255), nullable=False)
	owner_id = Column(Integer, nullable=False)
	price_per_day = Column(Float, nullable=False)

	def __init__(self, type, owner, owner_id, price_per_day):
		self.type = type
		self.owner = owner
		self.owner_id = owner_id
		self.price_per_day = price_per_day

	def serialize(self):
		return {
			'id': self.id,
			'type': self.type,
			'owner': self.owner,
			'owner_id': self.owner_id,
			'price_per_day': self.price_per_day
		}




