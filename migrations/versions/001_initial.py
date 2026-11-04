"""Initial schema.

Revision ID: 001
Revises:
"""
from alembic import op
from app.database import Base
from app import models  # noqa: F401
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)

def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
