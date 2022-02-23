from typing import List
from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, create_engine
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
import urllib.parse

from core.schemas.schema import TimezoneUpdate, UserUpdate
from settings import env_vars
from core.exceptions import NotFound

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    timezones = relationship(
        "Timezone", back_populates="owner", cascade="all, delete-orphan")


class Timezone(Base):
    __tablename__ = "timezones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city_name = Column(String)
    gmt_hours_diff = Column(Numeric)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="timezones")


class Repo(ABC):

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User, pwd: str, salt: str) -> None:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def create_timezone(self, tz: Timezone) -> Timezone:
        pass

    @abstractmethod
    def update_timezone(self, tz: Timezone) -> Timezone:
        pass

    @abstractmethod
    def list_timezone_by_user_id(self, user_id: int) -> Timezone:
        pass

    @abstractmethod
    def delete_timezone(self, tz_id: int) -> None:
        pass

    @abstractmethod
    def list_users(self) -> List[User]:
        pass


class PostgresRepo(Repo):
    def __init__(self) -> None:
        url_str = f"postgresql://{urllib.parse.quote_plus(env_vars.db_login)}:{urllib.parse.quote_plus(env_vars.db_password)}"\
            + f"@{env_vars.db_url}/{env_vars.db_name}"
        engine = create_engine(url_str)
        self.session = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)

    def list_users(self) -> List[User]:
        with self.session() as db:
            return db.query(User).all()

    def get_user_by_email(self, email: str) -> User:
        with self.session() as db:
            return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str) -> User:
        with self.session() as db:
            return db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: User) -> User:
        with self.session() as db:
            db.add(user)
            return self._commit_and_return_refreshed(db, user)

    def update_user(self, user: UserUpdate, pwd: str, salt: str) -> None:
        with self.session() as db:
            existing_user = db.query(User).filter(User.id == user.id).first()
            if existing_user is None:
                raise NotFound("User not found.")
            existing_user.email = user.email
            existing_user.password = pwd
            existing_user.salt = salt
            existing_user.is_admin = user.is_admin
            db.commit()

    def delete_user(self, user_id: int) -> None:
        with self.session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise NotFound("User was not found in DB.")
            self._delete_and_commit(db, user)

    def create_timezone(self, tz: Timezone) -> Timezone:
        with self.session() as db:
            db.add(tz)
            saved_tz = self._commit_and_return_refreshed(db, tz)
            return db.query(Timezone).options(joinedload(Timezone.owner)).filter(Timezone.id == saved_tz.id).first()

    def list_timezone_by_user_id(self, user_id: int) -> Timezone:
        with self.session() as db:
            return db.query(Timezone).filter(Timezone.owner_id == user_id).all()

    def update_timezone(self, tz: TimezoneUpdate) -> None:
        with self.session() as db:
            tz_model = db.query(Timezone).filter(Timezone.id == tz.id).first()
            if tz_model is None:
                raise NotFound("Timezone not found.")
            tz_model.gmt_hours_diff = tz.gmt_hours_diff
            tz_model.city_name = tz.city_name
            tz_model.name = tz.name
            tz_model.owner_id = tz.owner_id
            self._commit_and_return_refreshed(db, tz_model)

    def delete_timezone(self, tz_id: int) -> None:
        with self.session() as db:
            tz = db.query(Timezone).filter(Timezone.id == tz_id).first()
            if tz is None:
                raise NotFound("Timezone not found.")
            self._delete_and_commit(db, tz)

    def _commit_and_return_refreshed(self, db, arg1):
        db.commit()
        db.refresh(arg1)
        return arg1

    def _delete_and_commit(self, db, arg) -> None:
        db.delete(arg)
        db.commit()


postgres_repo = PostgresRepo()
