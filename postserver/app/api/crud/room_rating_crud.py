from app.model.room_rating import RoomRating
from app.db import room_ratings_table, database

async def create(room_rating: RoomRating):
	query = room_ratings_table.insert().values(
		rating=room_rating.rating,
		room_id=room_rating.room_id,
		reviewer=room_rating.reviewer,
		reviewer_id=room_rating.reviewer_id
    )
	return await database.execute(query=query)
