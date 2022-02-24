import unittest

from fastapi import Request
from fastapi.testclient import TestClient

from core.service import UserService, TimezoneService
from db_mock import MockRepo
from main import app
from v1.endpoints.users import get_user_service
from v1.endpoints.timezones import get_timezone_service
from auth import JWTBearer
from test_service import TestBaseService


class MockJWTBearer:
    async def __call__(self, request: Request):
        return {
            "user_id": 1,
            "user_email": "test@test.com",
            "is_admin": True
        }


class TestBaseEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MockRepo()
        self.user_service = UserService(repo=self.repo)
        self.timezone_service = TimezoneService(repo=self.repo)
        self.client = TestClient(app)
        app.dependency_overrides[get_user_service] = self.override_get_user_service
        app.dependency_overrides[get_timezone_service] = self.override_get_timezone_service
        app.dependency_overrides[JWTBearer] = MockJWTBearer

    def override_get_user_service(self):
        return self.user_service

    def override_get_timezone_service(self):
        return self.timezone_service


class TestEndpoints(TestBaseEndpoint, TestBaseService):
    def setUp(self) -> None:
        TestBaseEndpoint.setUp(self)
        TestBaseService.setUp(self)

    def test_user_login(self):
        self._add_default_user()
        payload = {
            "email": self.email,
            "password": self.pwd
        }
        response = self.client.post("/v1/users/login", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_user_signup(self):
        payload = {
            "email": self.email,
            "password": self.pwd
        }
        response = self.client.post("/v1/users/signup", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_user_list(self):
        pass

    def test_user_create(self):
        pass

    def test_user_update(self):
        pass

    def test_user_delete(self):
        pass

    def test_tz_create(self):
        pass

    def test_tz_update(self):
        pass

    def test_tz_list(self):
        pass

    def test_tz_delete(self):
        pass
