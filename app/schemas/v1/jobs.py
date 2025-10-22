from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .common import JobStatus


class JobRead(BaseModel):
    id: int
    type: str
    status: JobStatus
    payload: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
