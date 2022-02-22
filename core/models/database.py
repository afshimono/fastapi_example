from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import env_vars

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    salt = Column(String)
    timezones = relationship(
        "Timezone", back_populates="owner", cascade="all, delete-orphan")


class Timezone(Base):
    __tablename__ = "timezones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city_name = Column(Boolean)
    gmt_hour_diff = Column(Numeric)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="timezones")
