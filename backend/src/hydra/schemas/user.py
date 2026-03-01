from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str
    full_name: str


class User(UserCreate):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
