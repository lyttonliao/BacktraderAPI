"""add constraint user table

Revision ID: 32865c18ede0
Revises: 2045decef909
Create Date: 2024-07-16 01:06:52.570864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32865c18ede0'
down_revision: Union[str, None] = '2045decef909'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
