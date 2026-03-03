from fastapi import APIRouter

from hydra.api.dependencies import UserServiceDep, UserIdDep
from hydra.schemas.user import UsersRead, UserRead, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")  # TODO: superuser dependency and pagination
async def get_users(service: UserServiceDep) -> UsersRead:
    users, count = await service.get_all()
    return UsersRead(
        data=[UserRead.model_validate(user) for user in users],
        count=count,
    )


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    service: UserServiceDep,
) -> UserPublic:
    user = await service.get_by_id(user_id)
    return UserPublic.model_validate(user)
