import datetime as dt
import unittest
from unittest import mock

from fastapi.exceptions import HTTPException

from auth import (JWTBearer, JWTTokenHandler, hash_pwd,
                  check_logged_is_admin, check_logged_own_or_is_admin)


class TestAuth(unittest.TestCase):
    def setUp(self) -> None:
        self.jwt_secret = 'top_secret'
        self.jwt_handler = JWTTokenHandler(secret=self.jwt_secret)
        self.jwt_payload = {
            "user_id": 1,
            "is_admin": True,
            "email": "test@test.com"
        }
        self.jwt_date = dt.datetime(2022, 2, 12, 0, 0, 0)
        self.jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJpc19hZG1pbiI6dH'\
            'J1ZSwiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwIjoxNjQ0NjMxMjAwfQ.4yWuZCHGBXFZFCwuTRaDsvgW4VosnIcjlqnvA-IjXfQ'
        self.pwd = 'ultra_secret'
        self.salt = '$2b$12$26Yud1CKvrxQwdtGN4TrHe'
        self.pepper = 'pepper'
        self.hashed_pwd = '$2b$12$26Yud1CKvrxQwdtGN4TrHe4k5iXHFHeQqwfdSMaRTVdYo.jYIBoS.'

    @mock.patch('auth.dt.datetime')
    def test_create_jwt(self, mock_dt):
        mock_dt.utcnow = unittest.mock.Mock(return_value=self.jwt_date)
        jwt = self.jwt_handler.create_access_token(data=self.jwt_payload)
        self.assertEqual(jwt, self.jwt_token)

    def test_decode_token(self):
        new_token = self.jwt_handler.create_access_token(data=self.jwt_payload)
        decoded = self.jwt_handler.decode_access_token(new_token)
        del decoded["exp"]
        self.assertEqual(decoded, self.jwt_payload)
        with self.assertRaises(HTTPException) as context:
            self.jwt_handler.decode_access_token(self.jwt_token)

    def test_hash_pwd(self):
        hashed_pwd = hash_pwd(self.pwd, self.salt, self.pepper)
        self.assertEqual(hashed_pwd, self.hashed_pwd)

    def test_validate_logged_users(self):
        check_logged_is_admin(self.jwt_payload)
        check_logged_own_or_is_admin(self.jwt_payload, 1)
        self.jwt_payload.update({"is_admin": False})
        with self.assertRaises(HTTPException) as context:
            check_logged_is_admin(self.jwt_payload)

        with self.assertRaises(HTTPException) as context:
            check_logged_own_or_is_admin(self.jwt_payload, 2)
