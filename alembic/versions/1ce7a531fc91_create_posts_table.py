"""create posts table

Revision ID: 1ce7a531fc91
Revises: 
Create Date: 2023-11-19 21:47:51.964883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ce7a531fc91'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column(
        'id', sa.Integer(), nullable=False, primary_key=True), sa.Column(
        'title', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
