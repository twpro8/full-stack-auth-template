class HydraError(Exception):
    detail: str = "Unexpected error"

    def __init__(self, detail: str | None = None, *args: object) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail, *args)


class ObjectNotFoundError(HydraError):
    detail = "Object not found"


class ObjectAlreadyExistsError(HydraError):
    detail = "Object already exists"
