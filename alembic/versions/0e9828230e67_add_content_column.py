"""add content column

Revision ID: 0e9828230e67
Revises: f7325828c285
Create Date: 2026-06-16 12:52:58.886855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e9828230e67'
down_revision: Union[str, Sequence[str], None] = 'f7325828c285'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
