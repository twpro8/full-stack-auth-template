from fastapi import APIRouter, status, Depends
from fastapi.responses import Response

from hydra.api.dependencies import AuthServiceDep, get_current_user_id
from hydra.schemas.auth import RegisterForm, LoginForm
from hydra.schemas.common import SuccessResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate(
    form_data: LoginForm,
    service: AuthServiceDep,
    response: Response,
) -> SuccessResponse:
    # TODO: Create refresh token as well
    access_token = await service.login(
        email=form_data.email,
        password=form_data.password,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return SuccessResponse()


@router.post("/register", status_code=status.HTTP_201_CREATED)
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


# TODO: Refresh access token


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(get_current_user_id)
    ],  # check if there is a valid access token and user logged in
)
async def logout(response: Response) -> None:
    # TODO: Invalidate (revoke) refresh token
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="strict",
    )
