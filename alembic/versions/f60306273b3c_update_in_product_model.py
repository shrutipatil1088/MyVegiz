"""update in product model

Revision ID: f60306273b3c
Revises: cb959edfd487
Create Date: 2026-01-22 12:22:58.673500
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f60306273b3c'
down_revision: Union[str, Sequence[str], None] = 'cb959edfd487'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "products",
        "sub_category_id",
        existing_type=sa.Integer(),
        nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "products",
        "sub_category_id",
        existing_type=sa.Integer(),
        nullable=False
    )
