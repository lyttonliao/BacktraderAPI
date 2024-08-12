"""create strategy table

Revision ID: 5298842033c5
Revises: 
Create Date: 2024-08-01 16:32:20.327270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5298842033c5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'strategies',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False, index=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('public', sa.Boolean(), nullable=False, default=False, index=True),
        sa.Column('tags', sa.ARRAY(sa.String)),
        sa.Column('user_id', sa.Integer, index=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('version', sa.Integer, nullable=False, default=1),
        sa.UniqueConstraint('user_id', 'name', name='uq_user_id_name')
    )



def downgrade() -> None:
    op.drop_table('strategies')