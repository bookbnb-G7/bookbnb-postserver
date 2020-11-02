from app.model.room import Room


class RoomDAO:

	@classmethod
	def add_new_room(cls, db, room_args): 
		new_room = Room(type=room_args.type,
			            owner=room_args.owner,
			            owner_id=room_args.owner_id,
			            price_per_day=room_args.price_per_day)

		db.add(new_room)
		db.commit()

		return new_room.serialize()

	@classmethod
	def get_room(cls, db, room_id):
		room = db.query(Room).get(room_id)
		return room.serialize()