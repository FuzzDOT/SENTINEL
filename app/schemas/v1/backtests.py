from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BacktestRead(BaseModel):
    id: int
    name: str
    started_at: datetime
    finished_at: Optional[datetime]

    class Config:
        orm_mode = True
