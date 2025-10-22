from pydantic import BaseModel
from datetime import datetime


class SignalRead(BaseModel):
    id: int
    asset_id: int
    score: float
    ts: datetime

    class Config:
        orm_mode = True
