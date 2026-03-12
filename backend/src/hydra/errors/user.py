from hydra.errors import ObjectNotFoundError, ObjectAlreadyExistsError


class UserAlreadyExistsError(ObjectAlreadyExistsError):
    detail = "User already exists"


class UserNotFoundError(ObjectNotFoundError):
    detail = "User not found"
