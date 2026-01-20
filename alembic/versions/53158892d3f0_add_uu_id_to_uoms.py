"""add uu_id to uoms

Revision ID: 53158892d3f0
Revises: 8a2c7365d89f
Create Date: 2026-01-20 17:43:27.504210
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = "53158892d3f0"
down_revision: Union[str, Sequence[str], None] = "8a2c7365d89f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1️⃣ Add column as nullable first
    op.add_column(
        "uoms",
        sa.Column("uu_id", sa.String(255), nullable=True)
    )

    # 2️⃣ Backfill existing rows
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id FROM uoms"))

    for row in result:
        conn.execute(
            sa.text("""
                UPDATE uoms
                SET uu_id = :uuid
                WHERE id = :id
            """),
            {
                "uuid": str(uuid.uuid4()),
                "id": row.id
            }
        )

    # 3️⃣ Enforce NOT NULL
    op.alter_column("uoms", "uu_id", nullable=False)

    # 4️⃣ Add UNIQUE index
    op.create_index(
        "ix_uoms_uu_id",
        "uoms",
        ["uu_id"],
        unique=True
    )


def downgrade() -> None:
    op.drop_index("ix_uoms_uu_id", table_name="uoms")
    op.drop_column("uoms", "uu_id")
