from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int


class PaginationParams(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 50
