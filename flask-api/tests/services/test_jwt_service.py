'''
    Defines JWT Service Tests.
'''

import pytest

from flask_jwt_extended import decode_token

from app.services.jwt import JWTService
from tests.helpers import add_user_to_db, remove_user_from_db

class TestJWTService:
    '''
        Tests for the JWT Service.
    '''
    service = JWTService()

    @pytest.mark.usefixtures("app_ctx")
    def test_access_refresh_create(self):
        '''
            Tests access and refresh token creation.
        '''
        user = add_user_to_db('usertwo', '21@email.com', 'testpassword')
        tokens = self.service.generate_access_refresh(user.id)

        assert tokens.get('access') and tokens.get('refresh')

        remove_user_from_db(user)

    @pytest.mark.usefixtures("app_ctx")
    def test_access_create(self):
        '''
            Tests access token creation.
        '''
        user = add_user_to_db('usertwo', '21@email.com', 'testpassword')
        tokens = self.service.generate_access_refresh(user.id)

        access = self.service.generate_access(tokens['refresh'], user.id)

        assert access

        remove_user_from_db(user)

    @pytest.mark.usefixtures("app_ctx")
    def test_token_blacklist(self):
        '''
            Tests token blacklisting.
        '''
        user = add_user_to_db('usertwo', '21@email.com', 'testpassword')
        tokens = self.service.generate_access_refresh(user.id)

        decoded_access = decode_token(tokens['access'])
        decoded_refresh = decode_token(tokens['refresh'])

        self.service.blacklist_token(decoded_access)

        assert self.service.is_token_revoked(decoded_access['jti'])
        assert not self.service.is_token_revoked(decoded_refresh['jti'])
