from app.model.room_review import RoomReview
from app.db import room_reviews_table, database

async def create(room_review: RoomReview):
	query = room_reviews_table.insert().values(
		review=room_review.review,
		room_id=room_review.room_id,
		reviewer=room_review.reviewer,
		reviewer_id=room_review.reviewer_id
    )
	return await database.execute(query=query)
