from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from app.models.models import Asset, ModelRegistry
from app.schemas.v1.assets import AssetRead
from app.schemas.v1.models import ModelRead
from app.schemas.v1.models import ModelCreate
from app.schemas.v1.assets import AssetCreate
from app.db import get_engine
from sqlmodel import Session, select

router = APIRouter(prefix="/catalog")


@router.get("/assets", response_model=List[AssetRead])
def list_catalog_assets(page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=1000)):
    engine = get_engine()
    offset = (page - 1) * size
    with Session(engine) as session:
        assets = session.exec(select(Asset).offset(offset).limit(size)).all()
    return assets


@router.post("/assets", response_model=AssetRead, status_code=201)
def create_asset(payload: AssetCreate):
    engine = get_engine()
    with Session(engine) as session:
        a = Asset(symbol=payload.symbol, name=payload.name, exchange=payload.exchange)
        session.add(a)
        session.commit()
        session.refresh(a)
    return a


@router.get("/models", response_model=List[ModelRead])
def list_models(stage: Optional[str] = Query(None), page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=1000)):
    engine = get_engine()
    offset = (page - 1) * size
    with Session(engine) as session:
        q = select(ModelRegistry)
        if stage:
            q = q.where(ModelRegistry.stage == stage)
        items = session.exec(q.offset(offset).limit(size)).all()
    return items


@router.post("/models", response_model=ModelRead, status_code=201)
def register_model(payload: ModelCreate):
    engine = get_engine()
    with Session(engine) as session:
        m = ModelRegistry(name=payload.name, version=payload.version, stage=payload.stage)
        session.add(m)
        session.commit()
        session.refresh(m)
    return m
