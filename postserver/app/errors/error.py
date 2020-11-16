from starlette.exceptions import HTTPException

class NotFoundError(HTTPException):
    message = 'not found'

    def __init__(self):
    	super().__init__(status_code=404,
    					 detail=self.message)