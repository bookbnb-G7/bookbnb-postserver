from app.model.room import Room
from app.errors.http_error import NotFoundError
from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from app.model.room_booking import RoomBooking
import datetime

# Radius of 1 is aprox 111km, so we take search for rooms that are
# within an 11km distance by using a radius of 0.1
RADIUS = 0.1


def validate_date_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        # Incorrect data format, should be YYYY-MM-DD
        return False


class RoomDAO:
    @classmethod
    def add_new_room(cls, db, room_args):
        new_room = Room(
            id=room_args.id,
            type=room_args.type,
            owner=room_args.owner,
            latitude=room_args.latitude,
            longitude=room_args.longitude,
            owner_uuid=room_args.owner_uuid,
            price_per_day=room_args.price_per_day,
            capacity=room_args.capacity,
        )

        db.add(new_room)
        db.commit()

        return new_room.serialize()

    @classmethod
    def get_room(cls, db, room_id):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        return room.serialize()

    @classmethod
    def delete_room(cls, db, room_id):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        db.delete(room)
        db.commit()

        return room.serialize()

    @classmethod
    def update_room(cls, db, room_id, update_args):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        # we should see if is necessary to update
        # owner and owner id. May be this should
        # be a restricted method)

        if update_args.type is not None:
            room.type = update_args.type

        if update_args.price_per_day is not None:
            room.price_per_day = update_args.price_per_day

        if ((update_args.longitude is not None) and
            (update_args.latitude is not None) and
            (-180 < update_args.longitude < 180) and
            (-90 < update_args.latitude < 90)
        ):
            room.location = WKTElement(
                f'POINT({update_args.longitude} {update_args.latitude})',
                srid=4326
            )

        if update_args.capacity is not None:
            room.capacity = update_args.capacity

        db.commit()

        return room.serialize()

    @classmethod
    def get_all_rooms(cls, db, date_from, date_to, longitude, latitude, people, owner_uuid):

        partial_query = db.query(Room)

        # Date query
        if ((date_from is not None) and
            (date_to is not None) and
            (validate_date_format(date_from)) and
            (validate_date_format(date_to)) and
            (datetime.datetime.strptime(date_from, '%Y-%m-%d') <= datetime.datetime.strptime(date_to, '%Y-%m-%d'))
        ):
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            # Get the list of room ids that are booked between the dates received
            book_list = db.query(RoomBooking) \
                .filter(((RoomBooking.date_from <= date_to) &
                         (RoomBooking.date_to >= date_from))) \
                .distinct(RoomBooking.room_id) \
                .with_entities(RoomBooking.room_id) \
                .all()
            # Turn the list of tuples into a list
            for i in range(len(book_list)):
                book_list[i] = book_list[i][0]
            # Filter the rooms that are not booked in the range
            partial_query = partial_query.filter(~ Room.id.in_(book_list))

        # Location query
        if ((longitude is not None) and
            (latitude is not None) and
            (-180 < longitude < 180) and
            (-90 < latitude < 90)
        ):
            point = WKTElement(f'POINT({longitude} {latitude})', srid=4326)
            partial_query = partial_query.filter(func.ST_DWithin(Room.location, point, RADIUS))

        # People capacity query
        if ((people is not None) and
            (people >= 0)
        ):
            partial_query = partial_query.filter(Room.capacity >= people)

        # Owner uuid query
        if owner_uuid is not None:
            partial_query = partial_query.filter(Room.owner_uuid == owner_uuid)

        rooms_list = partial_query.all()

        serialized_list = []
        for room in rooms_list:
            serialized_list.append(room.serialize())

        return serialized_list

    @classmethod
    def room_is_present(cls, db, room_id):
        room = db.query(Room).get(room_id)
        return room is not None
