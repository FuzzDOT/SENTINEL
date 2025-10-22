from fastapi import APIRouter, Query
from typing import Optional, List
from app.models.models import ModelRegistry
from app.schemas.v1.models import ModelRead
from app.schemas.v1.common import ModelStage
from app.db import get_engine
from sqlmodel import Session, select

router = APIRouter(prefix="/models")


@router.get("/", response_model=List[ModelRead])
def list_models(stage: Optional[ModelStage] = Query(None), page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=1000)):
    engine = get_engine()
    offset = (page - 1) * size
    with Session(engine) as session:
        q = select(ModelRegistry)
        if stage:
            q = q.where(ModelRegistry.stage == stage.value)
        items = session.exec(q.offset(offset).limit(size)).all()
    return items
