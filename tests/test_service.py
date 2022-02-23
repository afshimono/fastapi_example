import pwd
import unittest

from core.schemas.schema import UserCreate, UserUpdate
from core.models.database import User
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


class TestService(TestBaseService):

    def setUp(self) -> None:
        super().setUp()

    def _add_default_user(self):
        self.repo.users[1] = self.default_user

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
        pass

    def test_list_tz_by_user_id(self):
        pass

    def test_create_tz(self):
        pass

    def test_update_tz(self):
        pass

    def test_delete_tz(self):
        pass
