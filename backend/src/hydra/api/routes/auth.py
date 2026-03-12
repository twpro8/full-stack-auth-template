from fastapi import APIRouter, status
from fastapi.responses import Response

from hydra.api.dependencies import AuthServiceDep
from hydra.schemas.auth import RegisterForm, LoginForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate(
    form_data: LoginForm,
    service: AuthServiceDep,
    response: Response,
) -> dict[str, str]:
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
    return {"status": "OK"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    form_data: RegisterForm,
    service: AuthServiceDep,
) -> dict[str, str]:
    await service.register(
        full_name=form_data.full_name,
        email=form_data.email,
        password=form_data.password,
    )
    return {"status": "OK"}
