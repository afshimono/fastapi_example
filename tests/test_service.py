import pwd
from unicodedata import name
import unittest

from core.schemas.schema import TimezoneCreate, TimezoneUpdate, UserCreate, UserUpdate
from core.models.database import User, Timezone
from core.service import UserService, TimezoneService
from db_mock import MockRepo
from core.exceptions import NotFound, AuthError


class TestBaseService(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MockRepo()
        self.user_service = UserService(repo=self.repo)
        self.timezone_service = TimezoneService(repo=self.repo)

        # user const
        self.email = 'test@test.com'
        self.pwd = 'Test123!@#'
        self.salt = '$2b$12$26Yud1CKvrxQwdtGN4TrHe'
        self.hashed_pwd = '$2b$12$26Yud1CKvrxQwdtGN4TrHetyBaBswJ3xZOKG7guwHMIKjCkxMOOdi'
        self.user_create = UserCreate(
            email=self.email,
            password=self.pwd,
            is_admin=True
        )
        self.default_user = User(
            email=self.email,
            password=self.hashed_pwd,
            salt=self.salt,
            is_admin=True,
            id=1
        )

        # timezone const
        self.tz_name = "test"
        self.tz_city = "test city"
        self.tz_gmt_diff = -3
        self.default_timezone = Timezone(
            id=1,
            owner_id=1,
            name=self.tz_name,
            city_name=self.tz_city,
            gmt_hours_diff=self.tz_gmt_diff
        )

    def _add_default_user(self):
        self.repo.users[1] = self.default_user

    def _add_default_timezone(self):
        self.repo.timezones[1] = self.default_timezone


class TestService(TestBaseService):

    def setUp(self) -> None:
        super().setUp()

    def test_verify_pwd(self):
        self._add_default_user()
        user = self.user_service.verify_pwd(self.pwd, self.email)
        self.assertEqual(user.email, self.email)
        with self.assertRaises(AuthError) as context:
            self.user_service.verify_pwd('wrong_pass', self.email)
        with self.assertRaises(NotFound) as context:
            self.user_service.verify_pwd('any_pass', 'wrong_mail@test.com')

    def test_list_users(self):
        user1 = self.user_service.create_user(self.user_create)
        self.user_create.email = 'test2@test.com'
        user2 = self.user_service.create_user(self.user_create)
        user_list = self.user_service.list_users()
        email_list = [user.email for user in user_list]
        self.assertIn(user1.email, email_list)
        self.assertIn(user2.email, email_list)

    def test_get_user_by_email(self):
        self._add_default_user()
        user = self.user_service.get_user_by_email(self.email)
        self.assertEqual(self.email, user.email)

    def test_create_user(self):
        user = self.user_service.create_user(self.user_create)
        db_user = self.repo.users[1]
        self.assertEqual(user.email, db_user.email)

    def test_update_user(self):
        self._add_default_user()
        user_update = UserUpdate(
            email=self.email,
            id=1,
            is_admin=True,
            password=self.pwd
        )
        self.user_service.update_user(user_update)
        self.assertTrue(self.repo.users[1].is_admin)
        with self.assertRaises(NotFound) as context:
            user_update.id = 5
            self.user_service.update_user(user_update)

    def test_delete_user(self):
        self.repo.users[1] = User(email=self.email, id=1)
        self.user_service.delete_user(1)
        self.assertEqual(len(self.repo.users), 0)

    def test_get_tz_by_id(self):
        self._add_default_user()
        self.repo.timezones[1] = self.default_timezone
        tz = self.timezone_service.get_tz_by_id(1)
        self.assertEqual(tz.id, 1)

    def test_list_tz_by_user_id(self):
        self._add_default_user()
        self.repo.timezones[1] = self.default_timezone
        tz_list = self.timezone_service.list_tz_by_user_id(1)
        self.assertEqual(len(tz_list), 1)

    def test_create_tz(self):
        self._add_default_user()
        tz_create = TimezoneCreate(
            gmt_hours_diff=self.tz_gmt_diff,
            name=self.tz_name,
            city_name=self.tz_city,
            owner_id=1
        )
        tz_created = self.timezone_service.create_tz(tz_create)
        self.assertEqual(tz_create.name, tz_created.name)
        self.assertEqual(tz_create.owner_id, tz_created.owner_id)
        self.assertEqual(tz_create.city_name, tz_created.city_name)
        self.assertEqual(tz_create.gmt_hours_diff, tz_created.gmt_hours_diff)

    def test_update_tz(self):
        self._add_default_user()
        self._add_default_timezone()
        tz_update = TimezoneUpdate(
            gmt_hours_diff=10,
            name=self.tz_name,
            city_name=self.tz_city,
            owner_id=1,
            id=1
        )
        self.timezone_service.update_tz(tz_update)
        self.assertEqual(self.repo.timezones[1].gmt_hours_diff, 10)

    def test_delete_tz(self):
        self._add_default_user()
        self._add_default_timezone()
        self.timezone_service.delete_tz(1)
        self.assertEqual(len(self.repo.timezones), 0)
