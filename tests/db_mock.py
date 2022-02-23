import email
from typing import List, Optional

from core.models.database import (Repo, User, Timezone)
from core.exceptions import NotFound
from core.schemas.schema import UserUpdate


class MockRepo(Repo):
    def __init__(self) -> None:  # sourcery skip: dict-literal
        self.users = dict()
        self.timezones = dict()

    def get_user_by_email(self, email: str) -> Optional[User]:
        user_list = [user for user in list(self.users.values())
                     if user.email == email]
        return user_list[0] if user_list else None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def create_user(self, user: User) -> User:
        id = len(self.users.keys()) + 1
        user.id = id
        self.users[id] = user
        return user

    def update_user(self, user: UserUpdate, pwd: str, salt: str) -> None:
        if user.id not in self.users:
            raise NotFound("User not found.")

        self.users[user.id] = User(
            email=user.email,
            password=pwd,
            salt=salt,
            id=user.id,
            is_admin=user.is_admin
        )

    def delete_user(self, user_id: int) -> None:
        del self.users[user_id]

    def create_timezone(self, tz: Timezone) -> Timezone:
        id = len(self.users.keys()) + 1
        tz.id = id
        self.timezones[id] = User
        return tz

    def update_timezone(self, tz: Timezone) -> Timezone:
        if tz.id not in self.timezones:
            raise NotFound("Timezone not found.")
        self.timezones[tz.id] = tz

    def list_timezone_by_user_id(self, user_id: int) -> Timezone:
        return [tz for tz in list(self.timezones.values())
                if tz.dict()['owner_id'] == user_id]

    def delete_timezone(self, tz_id: int) -> None:
        del self.timezones[tz_id]

    def list_users(self) -> List[User]:
        return self.users.values()

    def get_timezone_by_id(self, tz_id: int) -> Timezone:
        return self.timezones.get(tz_id)
