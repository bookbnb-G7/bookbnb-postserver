from app.model.room import Room
from app.db import rooms_table, database

async def create(room: Room):
	query = rooms_table.insert().values(
		price_per_day=room.price_per_day,	
		accommodation_type=room.accommodation_type
	)
	return await database.execute(query=query)

async def read(room_id: int):
	query = rooms_table.select().where(
		room_id == rooms_table.c.id
	)
	
	room_data = await database.fetch_one(query=query)	

	price_per_day = room_data['price_per_day']
	accommodation_type = room_data['accommodation_type']

	return Room(accommodation_type, price_per_day)
