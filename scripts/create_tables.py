
from sqlalchemy import ForeignKey, Numeric, Table, Column, Integer, String, Boolean, MetaData, create_engine
import urllib.parse

import settings

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
