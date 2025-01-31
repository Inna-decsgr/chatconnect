"""Add favorite_users table

Revision ID: 805309343ace
Revises: 0cf1c9adac73
Create Date: 2025-01-31 14:45:39.605275

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '805309343ace'
down_revision = '0cf1c9adac73'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('favorite_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('favorite_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['favorite_id'], ['Users.user_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'favorite_id')
    )

def downgrade():
    op.drop_table('favorite_users')  # ❌ 롤백할 때만 삭제하도록 유지