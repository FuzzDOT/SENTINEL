"""initial

Revision ID: 0001
Revises: 
Create Date: 2025-10-22
"""
from alembic import op
import sqlalchemy as sa
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.db import get_engine
from app.models import models as models_module

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create all tables from SQLModel metadata as a simple initial migration
    engine = get_engine()
    models_module.SQLModel.metadata.create_all(engine)


def downgrade():
    engine = get_engine()
    models_module.SQLModel.metadata.drop_all(engine)
