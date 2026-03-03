from fastapi import APIRouter, Depends

from hydra.api.dependencies import (
    UserServiceDep,
    UserDep,
    get_current_superuser,
)
from hydra.schemas.user import UsersRead, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "", dependencies=[Depends(get_current_superuser)]
)  # TODO: implement pagination
async def get_users(service: UserServiceDep) -> UsersRead:
    users, count = await service.get_all()
    return UsersRead(
        data=[UserRead.model_validate(user) for user in users],
        count=count,
    )


@router.get("/me")
async def get_me(current_user: UserDep) -> UserRead:
    return UserRead.model_validate(current_user)
