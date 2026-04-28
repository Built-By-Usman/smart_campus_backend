"""added rejection_reason to complaints

Revision ID: fc74dab9f526
Revises: 
Create Date: 2026-04-28 17:16:26.395390

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'fc74dab9f526'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('complaints', sa.Column('rejection_reason', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('complaints', 'rejection_reason')