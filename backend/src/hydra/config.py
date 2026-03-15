import secrets
from typing import Annotated, Any

from pydantic import AnyUrl, BeforeValidator, computed_field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(value: Any) -> list[str] | str:
    if isinstance(value, str) and not value.startswith("["):
        return [i.strip() for i in value.split(",") if i.strip()]
    elif isinstance(value, list | str):
        return value
    raise ValueError(value)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = "Hydra Auth API"
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "http://localhost:5173"

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str
    PG_PASS: str
    DB_NAME: str

    @computed_field  # type: ignore
    @property
    def DB_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.PG_USER,
            password=self.PG_PASS,
            host=self.PG_HOST,
            port=self.PG_PORT,
            path=self.DB_NAME,
        )

    JWT_SECRET: str = secrets.token_urlsafe(128)
    JWT_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field  # type: ignore
    @property
    def ALL_CORS_ORIGINS(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    @computed_field  # type: ignore
    @property
    def OPENAPI_URL(self) -> str:
        return f"{self.API_V1_STR}/openapi.json"


settings = Settings()
