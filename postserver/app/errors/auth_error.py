class AuthException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class RevokedApiKeyError(AuthException):
	def __init__(self):
		message = "Revoked API key"
		super().__init__(status_code=400, detail=message)