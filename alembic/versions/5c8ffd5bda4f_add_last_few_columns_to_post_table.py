"""add last few columns to post table

Revision ID: 5c8ffd5bda4f
Revises: 5eae0a87d2cb
Create Date: 2026-06-16 20:34:47.143809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c8ffd5bda4f'
down_revision: Union[str, Sequence[str], None] = '5eae0a87d2cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('published',sa.Boolean(),nullable=False,server_default='True'),)
    op.add_column("posts",sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=True,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
