from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModelRead(BaseModel):
    id: int
    name: str
    version: str
    stage: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True



class ModelCreate(BaseModel):
    name: str
    version: str
    stage: Optional[str] = None

