from app.api.crud.room_dao import RoomDAO
from app.model.room_review import RoomReview
from app.errors.http_error import NotFoundError
from app.errors.bookbnb_error import NoRelationError


class RoomReviewDAO:
    @classmethod
    def add_new_room_review(cls, db, room_id, room_review_args):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        new_room_review = RoomReview(
            review=room_review_args.review,
            room_id=room_id,
            reviewer=room_review_args.reviewer,
            reviewer_id=room_review_args.reviewer_id,
        )

        db.add(new_room_review)
        db.commit()

        return new_room_review.serialize()

    @classmethod
    def get_all_reviews(cls, db, room_id):
        review_list = db.query(RoomReview).filter(room_id == RoomReview.room_id).all()

        serialized_list = []
        for review in review_list:
            serialized_list.append(review.serialize())

        return serialized_list

    @classmethod
    def get_room_review(cls, db, room_id, review_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_review = db.query(RoomReview).get(review_id)

        if room_review is None:
            raise NotFoundError("room review")

        if not room_review.is_from(room_id):
            raise NoRelationError("room", "room review")

        return room_review.serialize()

    @classmethod
    def delete_room_review(cls, db, room_id, review_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        room_review = db.query(RoomReview).get(review_id)

        if room_review is None:
            raise NotFoundError("room review")

        if not room_review.is_from(room_id):
            raise NoRelationError("room", "room review")

        db.delete(room_review)
        db.commit()

        return room_review.serialize()
