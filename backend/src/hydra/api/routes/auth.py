from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from hydra.api.dependencies import AuthServiceDep
from hydra.schemas.auth import RegisterForm, Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> Token:
    access_token = await service.login(
        username=form_data.username,
        password=form_data.password,
    )
    return Token(access_token=access_token)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    form_data: RegisterForm,
    service: AuthServiceDep,
) -> dict[str, str]:
    await service.register(
        username=form_data.username,
        password=form_data.password,
        email=form_data.email,
        full_name=form_data.full_name,
    )
    return {"status": "OK"}
