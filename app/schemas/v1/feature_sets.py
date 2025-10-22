from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FeatureSetRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
