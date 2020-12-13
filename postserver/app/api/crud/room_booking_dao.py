from datetime import date
from app.model.room import Room
from app.model.room_booking import RoomBooking
from app.errors.http_error import NotFoundError
from app.errors.bookbnb_error import RoomAlreadyBookedError, NoRelationError


class RoomBookingDAO:
    @classmethod
    def add_new_room_booking(cls, db, room_id, room_booking_args):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        # add validation about capacity

        booking_ends = room_booking_args.date_ends
        booking_begins = room_booking_args.date_begins

        bookings_on_same_date = db.query(RoomBooking) \
            .filter(RoomBooking.room_id == room_id) \
            .filter(RoomBooking.date_begins <= booking_begins,
                    RoomBooking.date_ends >= booking_begins,
                    RoomBooking.date_begins <= booking_ends,
                    RoomBooking.date_ends >= booking_ends) \
            .count()

        if bookings_on_same_date > 0:
            raise RoomAlreadyBookedError()

        booking_days = (booking_ends - booking_begins).days
        total_price = booking_days * room.price_per_day

        new_room_booking = RoomBooking(
            room_id=room_id,
            date_ends=booking_ends,
            date_begins=booking_begins,
            total_price = total_price,
            user_id=room_booking_args.user_id,
            amount_of_people=room_booking_args.amount_of_people
        )

        db.add(new_room_booking)
        db.commit()

        return new_room_booking.serialize()

    @classmethod
    def get_room_booking(cls, db, room_id, booking_id):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        room_booking = db.query(RoomBooking).get(booking_id)

        if room_booking is None:
            raise NotFoundError("room booking")

        if not room_booking.is_from(room_id):
            raise NoRelationError("room", "room booking")

        return room_booking.serialize()

    @classmethod
    def delete_room_booking(cls, db, room_id):
        room = db.query(Room).get(room_id)

        if room is None:
            raise NotFoundError("room")

        db.delete(room)
        db.commit()

        return room.serialize()

    @classmethod
    def get_all_room_bookings(cls, db):
        rooms_list = db.query(Room).all()

        serialized_list = []
        for room in rooms_list:
            serialized_list.append(room.serialize())

        return serialized_list

    @classmethod
    def get_all_room_bookings_from_user(cls, db):
        rooms_list = db.query(Room).all()

        serialized_list = []
        for room in rooms_list:
            serialized_list.append(room.serialize())

        return serialized_list

    @classmethod
    def get_all_room_bookings_from_room(cls, db):
        rooms_list = db.query(Room).all()

        serialized_list = []
        for room in rooms_list:
            serialized_list.append(room.serialize())

        return serialized_list

    @classmethod
    def room_is_present(cls, db, room_id):
        room = db.query(Room).get(room_id)
        return room is not None
