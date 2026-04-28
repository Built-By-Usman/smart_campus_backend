"""add message column to complaints

Revision ID: 0776aab1ba23
Revises: fc74dab9f526
Create Date: 2026-04-29 00:00:22.357533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0776aab1ba23'
down_revision: Union[str, Sequence[str], None] = 'fc74dab9f526'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('complaints', sa.Column('message', sa.String(), nullable=True))

    op.drop_column('complaints', 'rejection_reason')


def downgrade() -> None:
    """Downgrade schema."""
    
    op.add_column('complaints', sa.Column('rejection_reason', sa.VARCHAR(), autoincrement=False, nullable=True))

    op.drop_column('complaints', 'message')