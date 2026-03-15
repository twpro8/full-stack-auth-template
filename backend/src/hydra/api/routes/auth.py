from fastapi import APIRouter, status, Depends
from fastapi.responses import Response

from hydra.api.dependencies import (
    AuthServiceDep,
    RefreshTokenDep,
    require_not_authenticated,
    RefreshTokenOptionalDep,
)
from hydra.api.utilities import set_token_cookies, delete_token_cookies
from hydra.schemas.auth import RegisterForm, LoginForm
from hydra.schemas.common import SuccessResponse
from hydra.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_not_authenticated),
    ],
)
async def authenticate(
    form_data: LoginForm,
    service: AuthServiceDep,
    response: Response,
) -> UserRead:
    result = await service.login(email=form_data.email, password=form_data.password)
    set_token_cookies(response, result.access_token, result.refresh_token)
    return UserRead.model_validate(result.user)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_not_authenticated)],
)
async def register(
    form_data: RegisterForm,
    service: AuthServiceDep,
) -> SuccessResponse:
    await service.register(
        full_name=form_data.full_name,
        email=form_data.email,
        password=form_data.password,
    )
    return SuccessResponse()


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    refresh_token: RefreshTokenDep,
    service: AuthServiceDep,
    response: Response,
) -> SuccessResponse:
    tokens = await service.refresh(refresh_token)
    set_token_cookies(response, tokens.access_token, tokens.refresh_token)
    return SuccessResponse()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    refresh_token: RefreshTokenOptionalDep,
    service: AuthServiceDep,
    response: Response,
) -> None:
    delete_token_cookies(response)
    if refresh_token is None:
        return
    await service.logout(refresh_token)
