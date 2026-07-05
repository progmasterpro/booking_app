"""add unique email

Revision ID: 5f211038450d
Revises: 81c38ecb0de0
Create Date: 2026-02-17 23:19:16.056973

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "5f211038450d"
down_revision: Union[str, Sequence[str], None] = "81c38ecb0de0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
