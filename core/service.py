
import email
from typing import List

from bcrypt import gensalt

from core.schemas.schema import (UserBase,
                                 UserCreate, TimezoneUpdate, UserList, TimeZoneList,
                                 UserUpdate, TimezoneCreate, TimezoneBase)
from core.models.database import User, Timezone, Repo
from core.exceptions import InsertError, DeleteError, NotFound, AuthError
from auth import hash_pwd


class UserService:
    def __init__(self, repo: Repo) -> None:
        self.pepper = "951113620a6f3cdbb3d05401801b9fc8"
        self.repo = repo

    def verify_pwd(self, pwd: str, user_email: str) -> User:
        user = self.repo.get_user_by_email(user_email)
        if user is None:
            raise NotFound("User not found.")
        hashed_pwd = hash_pwd(pwd=pwd, salt=user.salt, pepper=self.pepper)
        if hashed_pwd != user.password:
            raise AuthError("Auth error: wrong password.")
        return user

    def list_users(self) -> List[UserList]:
        user_list = self.repo.list_users()
        return [UserList(email=user.email, id=user.id) for user in user_list]

    def get_user_by_email(self, email: str) -> User:
        return self.repo.get_user_by_email(email)

    def create_user(self, user: UserCreate) -> UserBase:
        existing_user = self.repo.get_user_by_email(user.email)
        if existing_user is not None:
            raise InsertError("User already exists.")
        salt = gensalt().decode('utf-8')
        pwd = hash_pwd(user.password, salt=salt, pepper=self.pepper)
        new_user = User(salt=salt, email=user.email,
                        password=pwd, is_admin=user.is_admin)
        user_entity = self.repo.create_user(user=new_user)
        return UserBase(
            email=user_entity.email
        )

    def update_user(self, user: UserUpdate) -> None:
        salt = gensalt().decode('utf-8')
        pwd = hash_pwd(user.password, salt=salt, pepper=self.pepper)
        self.repo.update_user(user, pwd=pwd, salt=salt)

    def delete_user(self, user_id: int) -> UserBase:
        try:
            self.repo.delete_user(user_id)
        except NotFound as e:
            raise DeleteError(e) from e

    def _create_user_entity(self, pwd: str, pepper: str, email: str, is_admin: bool) -> User:
        salt = gensalt().decode('utf-8')
        pwd = hash_pwd(pwd, salt=salt, pepper=pepper)
        return User(salt=salt, email=email,
                    password=pwd, is_admin=is_admin)


class TimezoneService:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo

    def list_tz_by_user_id(self, user_id: int) -> List[TimezoneUpdate]:
        tz_list = self.repo.list_timezone_by_user_id(user_id)
        return [TimezoneUpdate(name=tz.name, gmt_hours_diff=tz.gmt_hours_diff,
                               city_name=tz.city_name, owner_id=tz.owner_id, id=tz.id) for tz in tz_list]

    def create_tz(self, tz: TimezoneCreate) -> TimezoneUpdate:
        timezone = Timezone(**tz.dict())
        saved_entity = self.repo.create_timezone(timezone)
        return TimeZoneList(
            gmt_hours_diff=saved_entity.gmt_hours_diff,
            id=saved_entity.id,
            city_name=saved_entity.city_name,
            name=saved_entity.name,
            owner_id=saved_entity.owner_id,
            owner=UserBase(email=saved_entity.owner.email)
        )

    def update_tz(self, tz: TimezoneUpdate) -> None:
        self.repo.update_timezone(tz)

    def delete_tz(self, tz_id: int) -> None:
        self.repo.delete_timezone(tz_id=tz_id)
