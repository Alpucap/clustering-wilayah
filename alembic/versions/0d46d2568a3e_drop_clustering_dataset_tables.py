"""drop clustering dataset tables

Revision ID: 0d46d2568a3e
Revises: 66eb475e9f4a
Create Date: 2025-10-17 20:17:08.246485
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0d46d2568a3e"
down_revision: Union[str, Sequence[str], None] = "66eb475e9f4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("clustering_dataset_d")
    op.drop_table("clustering_dataset_h")


def downgrade() -> None:
    op.create_table(
        "clustering_dataset_h",
        sa.Column("clustering_dataset_h_id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("dataset_name", sa.String(100), nullable=False),
        sa.Column("description", sa.String(200)),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        "clustering_dataset_d",
        sa.Column("clustering_dataset_d_id", sa.Integer, primary_key=True, index=True),
        sa.Column("clustering_dataset_h_id", sa.Integer, sa.ForeignKey("clustering_dataset_h.clustering_dataset_h_id", ondelete="CASCADE"), nullable=False),
        sa.Column("tahun", sa.Integer, nullable=False),
        sa.Column("kabupaten_kota", sa.String(100), nullable=False),
        sa.Column("angka_harapan_hidup_l", sa.DECIMAL(5,2)),
        sa.Column("angka_harapan_hidup_p", sa.DECIMAL(5,2)),
        sa.Column("persentase_penduduk_miskin", sa.DECIMAL(5,2)),
        sa.Column("index_kedalaman_kemiskinan", sa.DECIMAL(5,2)),
        sa.Column("index_keparahan_kemiskinan", sa.DECIMAL(5,2)),
        sa.Column("rata_rata_lama_sekolah", sa.DECIMAL(5,2)),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
