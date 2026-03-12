from datetime import datetime

from hydra.schemas import BaseSchema


class UserCreate(BaseSchema):
    email: str
    password_hash: str
    full_name: str


class User(UserCreate):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime


class UserRead(BaseSchema):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime


class UsersRead(BaseSchema):
    count: int
    data: list[UserRead]


class UserPublic(BaseSchema):
    id: int
    email: str
    full_name: str
    created_at: datetime
