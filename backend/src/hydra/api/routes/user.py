from fastapi import APIRouter, Depends

from hydra.api.dependencies import (
    UserServiceDep,
    UserDep,
    get_current_superuser,
    PaginationDep,
)
from hydra.schemas.user import UsersRead, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", dependencies=[Depends(get_current_superuser)])
async def get_users(service: UserServiceDep, pagination: PaginationDep) -> UsersRead:
    result = await service.get_all(pagination.offset, pagination.page_size)
    return UsersRead(
        data=[UserRead.model_validate(user) for user in result.items],
        count=result.count,
    )


@router.get("/me")
async def get_me(current_user: UserDep) -> UserRead:
    return UserRead.model_validate(current_user)
