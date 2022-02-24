import unittest

from fastapi import Request
from fastapi.testclient import TestClient

from core.service import UserService, TimezoneService
from db_mock import MockRepo
from main import app
from v1.endpoints.users import get_user_service
from v1.endpoints.timezones import get_timezone_service
from auth import get_logged_credentials
from test_service import TestBaseService


class TestBaseEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MockRepo()
        self.user_service = UserService(repo=self.repo)
        self.timezone_service = TimezoneService(repo=self.repo)
        self.client = TestClient(app)
        app.dependency_overrides[get_user_service] = self.override_get_user_service
        app.dependency_overrides[get_timezone_service] = self.override_get_timezone_service
        app.dependency_overrides[get_logged_credentials] = self.override_logged_credentials

    def override_get_user_service(self):
        return self.user_service

    def override_get_timezone_service(self):
        return self.timezone_service

    async def override_logged_credentials(self):
        return {
            "user_id": 1,
            "user_email": "test@test.com",
            "is_admin": True
        }


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

    def test_user_signup(self):  # sourcery skip: class-extract-method
        payload = {
            "email": self.email,
            "password": self.pwd
        }
        response = self.client.post("/v1/users/signup", json=payload)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/v1/users/signup", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_user_list(self):
        self._add_default_user()
        response = self.client.get("/v1/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_user_create(self):
        payload = {"email": f'new_{self.email}',
                   "password": self.pwd, "is_admin": True}
        response = self.client.post("/v1/users/", json=payload)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/v1/users/", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_user_update(self):
        self._add_default_user()
        payload = {
            "id": 1,
            "email": "test2@test.com",
            "password": "Zxc123!!@@##",
            "is_admin": False
        }
        response = self.client.put("/v1/users/", json=payload)
        self.assertEqual(response.status_code, 204)

    def test_user_delete(self):
        self._add_default_user()
        response = self.client.delete("/v1/users/1")
        self.assertEqual(response.status_code, 204)

    def test_tz_create(self):
        self._add_default_user()

    def test_tz_update(self):
        self._add_default_user()

    def test_tz_list(self):
        self._add_default_user()

    def test_tz_delete(self):
        self._add_default_user()
