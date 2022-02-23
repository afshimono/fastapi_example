
from sqlalchemy import ForeignKey, Numeric, Table, Column, Integer, String, Boolean, MetaData, create_engine
import urllib.parse
from core.schemas.schema import UserCreate

import settings
from core.service import UserService
from core.models.database import postgres_repo

env_vars = settings.env_vars
url_str = f"postgresql://{urllib.parse.quote_plus(env_vars.db_login)}:{urllib.parse.quote_plus(env_vars.db_password)}"\
    + f"@{env_vars.db_url}/{env_vars.db_name}"
engine = create_engine(url_str)
meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, unique=True),
    Column('password', String, nullable=False),
    Column('salt', String, nullable=False),
    Column('is_admin', Boolean, nullable=False)
)

timezones = Table(
    'timezones', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('city_name', String),
    Column('gmt_hours_diff', Numeric),
    Column('owner_id', Integer, ForeignKey("users.id"), nullable=False)
)

meta.create_all(engine)

user_service = UserService(repo=postgres_repo)
user_service.create_user(UserCreate(
    email=env_vars.admin_email, password=env_vars.admin_pwd, is_admin=True))
