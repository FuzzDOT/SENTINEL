from fastapi import APIRouter
from typing import List
from app.models.models import FeatureSet
from app.schemas.v1.feature_sets import FeatureSetRead
from app.db import get_engine
from sqlmodel import Session, select

router = APIRouter(prefix="/data")


@router.get("/feature-sets", response_model=List[FeatureSetRead])
def list_feature_sets():
    engine = get_engine()
    with Session(engine) as session:
        items = session.exec(select(FeatureSet).limit(100)).all()
    return items
