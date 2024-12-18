from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    password: Optional[str]


class User(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        from_attributes = True
