from app.api.crud.room_dao import RoomDAO
from app.model.room_rating import RoomRating
from app.errors.http_error import NotFoundError
from app.errors.bookbnb_error import NoRelationError


class RoomRatingDAO:
    @classmethod
    def add_new_room_rating(cls, db, room_id, room_rating_args):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        new_room_rating = RoomRating(
            rating=room_rating_args.rating,
            room_id=room_id,
            reviewer=room_rating_args.reviewer,
            reviewer_id=room_rating_args.reviewer_id,
        )

        db.add(new_room_rating)
        db.commit()

        return new_room_rating.serialize()

    @classmethod
    def get_all_ratings(cls, db, room_id):
        rating_list = db.query(RoomRating).filter(room_id == RoomRating.room_id).all()

        serialized_list = []
        for rating in rating_list:
            serialized_list.append(rating.serialize())

        return serialized_list

    @classmethod
    def get_room_rating(cls, db, room_id, rating_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_rating = db.query(RoomRating).get(rating_id)

        if room_rating is None:
            raise NotFoundError("room rating")

        if not room_rating.is_from(room_id):
            raise NoRelationError("room", "room rating")

        return room_rating.serialize()

    @classmethod
    def delete_room_rating(cls, db, room_id, rating_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_rating = db.query(RoomRating).get(rating_id)

        if room_rating is None:
            raise NotFoundError("room rating")

        if not room_rating.is_from(room_id):
            raise NoRelationError("room", "room rating")

        db.delete(room_rating)
        db.commit()

        return room_rating.serialize()

    @classmethod
    def update_room_rating(cls, db, room_id, rating_id, update_args):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_rating = db.query(RoomRating).get(rating_id)

        if room_rating is None:
            raise NotFoundError("room rating")

        if not room_rating.is_from(room_id):
            raise NoRelationError("room", "room rating")

        if update_args.rating is not None:
            room_rating.rating = update_args.rating

        db.commit()

        return room_rating.serialize()
