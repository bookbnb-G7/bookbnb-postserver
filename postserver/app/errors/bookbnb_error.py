class BookbnbException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

class NoRelationError(BookbnbException):
    def __init__(self, item_b, item_a):
        message = f'no relation between {item_a} and {item_b}'
        super().__init__(status_code=200,
                         detail=message)