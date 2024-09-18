"""remove tag column, add inputs and params columns

Revision ID: 8cb4f8026735
Revises: 5298842033c5
Create Date: 2024-09-16 20:04:25.114133

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8cb4f8026735"
down_revision: Union[str, None] = "5298842033c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("strategies", "tags")
    op.add_column(
        "strategies",
        sa.Column("inputs", sa.ARRAY(sa.String), nullable=False, server_default="{}"),
    )
    op.add_column(
        "strategies", sa.Column("params", sa.JSON, nullable=False, server_default="{}")
    )

    # op.execute("UPDATE strategies SET inputs = '{}' WHERE inputs is NULL")
    # op.execute("UPDATE strategies SET params = '{}' WHERE params is NULL")


def downgrade() -> None:
    op.add_column("strategies", sa.Column("tags", sa.ARRAY(sa.String)))
    op.drop_column("strategies", "inputs")
    op.drop_column("strategies", "params")
