from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginForm(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(extra="forbid")


class RegisterForm(LoginForm):
    email: EmailStr = Field(max_length=128)
    full_name: str = Field(min_length=2, max_length=64)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
