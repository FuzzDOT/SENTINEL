from sqlmodel import create_engine, SQLModel
import os
from .core.settings import settings


def get_engine():
    url = os.getenv("DATABASE_URL") or str(settings.DATABASE_URL)
    # echo disabled by default; tests may enable by monkeypatching
    return create_engine(url, connect_args={"check_same_thread": False} if url.startswith("sqlite") else {}, echo=False)


def init_db():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    return engine
