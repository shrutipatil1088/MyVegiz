"""update products add fields

Revision ID: 3e24eb3a89fb
Revises: 1ea1c87ff2c4
Create Date: 2026-01-20 12:50:49.400638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e24eb3a89fb'
down_revision: Union[str, Sequence[str], None] = '1ea1c87ff2c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

import uuid


def upgrade() -> None:
    # 1️⃣ Add columns as NULLABLE
    op.add_column('products', sa.Column('uu_id', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('slug', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('short_description', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('long_description', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('hsm_code', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('sku_code', sa.String(255), nullable=True))

    # 2️⃣ Backfill existing rows
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id FROM products"))

    for row in result:
        conn.execute(
            sa.text("""
                UPDATE products
                SET
                    uu_id = :uuid,
                    slug = CONCAT('product-', id),
                    short_description = 'N/A',
                    long_description = 'N/A',
                    hsm_code = 'N/A',
                    sku_code = 'N/A'
                WHERE id = :id
            """),
            {
                "uuid": str(uuid.uuid4()),
                "id": row.id
            }
        )

    # 3️⃣ Enforce NOT NULL
    op.alter_column('products', 'uu_id', nullable=False)
    op.alter_column('products', 'slug', nullable=False)
    op.alter_column('products', 'short_description', nullable=False)
    op.alter_column('products', 'long_description', nullable=False)
    op.alter_column('products', 'hsm_code', nullable=False)
    op.alter_column('products', 'sku_code', nullable=False)

    # 4️⃣ Drop old column
    op.drop_column('products', 'product_image')

    # 5️⃣ Indexes (safe now)
    op.create_index('ix_products_uu_id', 'products', ['uu_id'], unique=True)
    op.create_index('ix_products_slug', 'products', ['slug'])
