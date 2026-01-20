"""add uu_id to users

Revision ID: 90a34b174975
Revises: 53158892d3f0
Create Date: 2026-01-20 18:17:25.450175
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = "90a34b174975"
down_revision: Union[str, Sequence[str], None] = "53158892d3f0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1️⃣ Add uu_id column as NULLABLE
    op.add_column(
        "users",
        sa.Column("uu_id", sa.String(255), nullable=True)
    )

    # 2️⃣ Backfill existing rows
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id FROM users"))

    for row in result:
        conn.execute(
            sa.text("""
                UPDATE users
                SET uu_id = :uuid
                WHERE id = :id
            """),
            {
                "uuid": str(uuid.uuid4()),
                "id": row.id
            }
        )

    # 3️⃣ Enforce NOT NULL
    op.alter_column("users", "uu_id", nullable=False)

    # 4️⃣ Create UNIQUE index
    op.create_index(
        "ix_users_uu_id",
        "users",
        ["uu_id"],
        unique=True
    )


def downgrade() -> None:
    op.drop_index("ix_users_uu_id", table_name="users")
    op.drop_column("users", "uu_id")
