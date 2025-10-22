from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AssetRead(BaseModel):
    id: int
    symbol: str
    name: Optional[str]
    exchange: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True



class AssetCreate(BaseModel):
    symbol: str
    name: Optional[str] = None
    exchange: Optional[str] = None

