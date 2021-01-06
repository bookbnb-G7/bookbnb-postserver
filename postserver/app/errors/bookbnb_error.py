class BookbnbException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class NoRelationError(BookbnbException):
    def __init__(self, item_b, item_a):
        message = f"no relation between {item_a} and {item_b}"
        super().__init__(status_code=400, detail=message)


class MainCommentIsAnswerError(BookbnbException):
    def __init__(self):
        message = f"an answer cant be a main comment"
        super().__init__(status_code=400, detail=message)


class RoomAlreadyBookedError(BookbnbException):
    def __init__(self):
        message = "the room is already booked on that date"
        super().__init__(status_code=400, detail=message)