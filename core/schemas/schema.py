import re
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, validator
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserList(UserBase):
    id: int


class UserSignUp(UserBase):
    password: str

    @validator('password')
    def strong_password(cls, v):
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$', v):
            raise ValueError(
                'Password must be at least 8 characters long, 18 characters max, and contain at least 1 Capital, 1 Special and 1 Number. ')
        return v


class UserCreate(UserSignUp):
    is_admin: bool


class UserUpdate(UserCreate, UserList):
    pass


class TimezoneBase(BaseModel):
    gmt_hours_diff: Decimal
    name: str
    city_name: str

    @validator('gmt_hours_diff')
    def check_range(cls, v):
        if v < -12 or v > 14:
            raise ValueError(
                'Value must not be smaller than 14 and greater than -12.')
        return v


class TimezoneCreate(TimezoneBase):
    owner_id: Optional[int]


class TimezoneUpdate(TimezoneCreate):
    id: int


class TimeZoneList(TimezoneUpdate):
    owner: UserBase
