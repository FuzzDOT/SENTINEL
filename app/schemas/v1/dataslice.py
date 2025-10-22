from pydantic import BaseModel
from datetime import datetime


class DataSliceRead(BaseModel):
    id: int
    name: str
    start: datetime
    end: datetime

    class Config:
        orm_mode = True
