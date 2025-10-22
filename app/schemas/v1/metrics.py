from pydantic import BaseModel
from datetime import datetime


class MetricRead(BaseModel):
    id: int
    name: str
    value: float
    ts: datetime

    class Config:
        orm_mode = True
