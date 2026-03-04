from hydra.errors import HydraError


class InvalidCredentialsError(HydraError):
    detail = "Invalid credentials"


class InvalidPasswordError(HydraError):
    detail = "Invalid password"
