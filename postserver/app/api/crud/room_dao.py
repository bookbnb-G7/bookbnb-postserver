from app.db import session
from app.model.room import Room


class RoomDAO:

	@classmethod
	def add_new_room(cls, room_args): 
		new_room = Room(type=room_args.type,
			            owner=room_args.owner,
			            owner_id=room_args.owner_id,
			            price_per_day=room_args.price_per_day)

		session.add(new_room)
		session.commit()

		return new_room.serialize()

	@classmethod
	def get_room(cls, room_id):
		room = session.query(Room).get(room_id)
		return room.serialize()