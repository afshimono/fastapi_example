import unittest

from core.service import UserService, TimezoneService
from db_mock import MockRepo


class TestBaseEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MockRepo()
        self.user_service = UserService(repo=self.repo)
        self.timezone_service = TimezoneService(repo=self.repo)


class TestEndpoints(TestBaseEndpoint):
    def setUp(self) -> None:
        return super().setUp()

    def test_user_login(self):
        pass

    def test_user_signup(self):
        pass

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
