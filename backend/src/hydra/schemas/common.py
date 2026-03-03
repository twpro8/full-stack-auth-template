from dataclasses import dataclass
from typing import Sequence

from pydantic import Field

from hydra.schemas import BaseSchema


class PaginationParams(BaseSchema):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, gt=0, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


@dataclass
class PaginatedResult[T]:
    items: Sequence[T]
    count: int
