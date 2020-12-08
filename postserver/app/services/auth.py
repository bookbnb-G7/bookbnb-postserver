import os
from app.errors.auth_error import RevokedApiKeyError

class AuthService():
    def __init__(self):
        self.api_key = '' #os.environ.get('API_KEY')

    def verify_apy_key(self, api_key):
        if api_key == self.api_key:
            return

        raise RevokedApiKeyError()


class AuthServiceFake():
    def verify_apy_key(self, api_key):
        return 


auth_service = None 
if (os.environ.get('ENVIRONMENT') == 'production'):
    auth_service = AuthService()
else:
    auth_service = AuthServiceFake()