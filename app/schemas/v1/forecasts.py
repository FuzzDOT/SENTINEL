from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ForecastRead(BaseModel):
    id: int
    model_id: int
    run_at: datetime
    payload: Optional[str]

    class Config:
        orm_mode = True
