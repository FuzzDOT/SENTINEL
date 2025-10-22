from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    name: Optional[str] = None
    exchange: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FeatureSet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ModelRegistry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    version: str
    stage: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    status: str
    payload: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Forecast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model_id: Optional[int] = Field(default=None, foreign_key="modelregistry.id")
    run_at: datetime = Field(default_factory=datetime.utcnow)
    payload: Optional[str] = None


class Signal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id")
    score: float
    ts: datetime = Field(default_factory=datetime.utcnow)


class BacktestRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None


class Metric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    value: float
    ts: datetime = Field(default_factory=datetime.utcnow)


class DataSlice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start: datetime
    end: datetime
