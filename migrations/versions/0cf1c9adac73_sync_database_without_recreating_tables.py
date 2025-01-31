"""Sync database without recreating tables

Revision ID: 0cf1c9adac73
Revises: 9e2c57c96c88
Create Date: 2025-01-31 14:28:03.960782

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0cf1c9adac73'
down_revision = '9e2c57c96c88'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass