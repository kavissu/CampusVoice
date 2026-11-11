"""add location reference to halls

Revision ID: 89da72dccace
Revises:
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "89da72dccace"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("halls", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("location_id", sa.Integer(), nullable=False)
        )

        batch_op.create_foreign_key(
            "fk_halls_location_id_locations",
            "locations",
            ["location_id"],
            ["id"],
        )

        batch_op.create_unique_constraint(
            "uq_halls_location_id",
            ["location_id"],
        )

        batch_op.drop_column("qr_code_token")


def downgrade() -> None:
    with op.batch_alter_table("halls", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("qr_code_token", sa.String(length=100), nullable=True)
        )

        batch_op.drop_constraint(
            "fk_halls_location_id_locations",
            type_="foreignkey",
        )

        batch_op.drop_constraint(
            "uq_halls_location_id",
            type_="unique",
        )

        batch_op.drop_column("location_id")