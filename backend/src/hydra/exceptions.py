class HydraError(Exception):
    detail: str = "Unexpected error."

    def __init__(self, detail: str | None = None, *args: object) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail, *args)


class InvalidCredentialsError(HydraError):
    detail = "Invalid credentials."


class InvalidPasswordError(HydraError):
    detail = "Invalid password."


class ObjectNotFoundError(HydraError):
    detail = "Object not found."


class ObjectAlreadyExistsError(HydraError):
    detail = "Object already exists."


class UserAlreadyExistsError(ObjectAlreadyExistsError):
    detail = "User already exists."


class UserNotFoundError(ObjectNotFoundError):
    detail = "User not found."
