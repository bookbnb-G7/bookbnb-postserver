from app.api.crud.room_dao import RoomDAO
from app.model.room_comment import RoomComment
from app.errors.http_error import NotFoundError
from app.errors.bookbnb_error import NoRelationError, \
                                     MainCommentIsAnswerError


class RoomCommentDAO:
    @classmethod
    def add_new_comment(cls, db, room_id, comment_args):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        if comment_args.main_comment_id is not None:
            if not cls.comment_is_present(db, comment_args.main_comment_id):
                raise NotFoundError("comment")

            main_comment = db.query(RoomComment).get(comment_args.main_comment_id)
            if main_comment.is_asnwer():
                raise MainCommentIsAnswerError()

        new_comment = RoomComment(
            comment=comment_args.comment,
            room_id=room_id,
            commentator=comment_args.commentator,
            commentator_id=comment_args.commentator_id,
            main_comment_id=comment_args.main_comment_id
        )

        db.add(new_comment)
        db.commit()

        return new_comment.serialize()

    @classmethod
    def get_comment_with_answers(cls, db, room_id, comment_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        comment = db.query(RoomComment).get(comment_id)

        answers = db.query(RoomComment) \
            .filter(comment.id == RoomComment.main_comment_id) \
            .all()

        serialized_answers = []
        for answer in answers:
            serialized_answers.append(answer.serialize())

        return {"comment": comment.serialize(), "answers": serialized_answers}

    @classmethod
    def get_all_comments(cls, db, room_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        main_comments = db.query(RoomComment) \
            .filter(room_id == RoomComment.room_id and
                    RoomComment.main_comment_id is None) \
            .all()

        all_comments = []
        for comment in main_comments:
            comment_with_answers = cls.get_comment_with_answers(db, room_id, comment.id)
            all_comments.append(comment_with_answers)

        return all_comments

    @classmethod
    def get_comment(cls, db, room_id, comment_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        comment = db.query(RoomComment).get(comment_id)

        if comment is None:
            raise NotFoundError("comment")

        if not comment.is_from(room_id):
            raise NoRelationError("room", "comment")

        return comment.serialize()

    @classmethod
    def delete_comment(cls, db, room_id, comment_id):
        if not RoomDAO.room_is_present(db, room_id):
            raise NotFoundError("room")

        comment = db.query(RoomComment).get(comment_id)

        if comment is None:
            raise NotFoundError("comment")

        if not comment.is_from(room_id):
            raise NoRelationError("room", "comment")

        db.delete(comment)

        if not comment.is_anwer():
            answers = db.query(RoomComment)\
                .filter(comment.id == RoomComment.main_comment_id)\
                .all()

            for answer in answers:
                db.delete(answer)

        db.commit()

        return comment

    @classmethod
    def comment_is_present(cls, db, comment_id):
        comment = db.query(RoomComment).get(comment_id)
        return comment is not None
