from app.model.room import Room
from app.db import rooms_table, database

async def create(room: Room):
	query = rooms_table.insert().values(
		price_per_day=room.price_per_day,	
		accommodation_type=room.accommodation_type
	)
	return await database.execute(query=query)
