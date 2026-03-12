from pydantic import ConfigDict, EmailStr, Field

from hydra.schemas import BaseSchema


class LoginForm(BaseSchema):
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(extra="forbid")


class RegisterForm(LoginForm):
    email: EmailStr = Field(max_length=128)
    full_name: str = Field(min_length=2, max_length=64)


class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseSchema):
    sub: int
