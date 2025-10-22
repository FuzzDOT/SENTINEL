from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config
if config and config.config_file_name:
    fileConfig(config.config_file_name)

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db import get_engine
from app.models import models as models_module


def run_migrations_offline():
    url = os.getenv("DATABASE_URL")
    context.configure(url=url, target_metadata=models_module.SQLModel.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=models_module.SQLModel.metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
