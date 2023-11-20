"""Add content column to posts table

Revision ID: 4f1f311ee179
Revises: 1ce7a531fc91
Create Date: 2023-11-20 08:15:57.818786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f1f311ee179'
down_revision: Union[str, None] = '1ce7a531fc91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", 'content')
