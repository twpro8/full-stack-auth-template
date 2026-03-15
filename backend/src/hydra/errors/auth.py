from hydra.errors import HydraError


class InvalidCredentialsError(HydraError):
    detail = "Invalid credentials"


class InvalidPasswordError(HydraError):
    detail = "Invalid password"


class InvalidRefreshTokenError(HydraError):
    detail = "Invalid refresh token"


class RefreshTokenRevokedError(HydraError):
    detail = "Refresh token revoked"
