"""Created incidents table

Revision ID: 8ba4934fdaa2
Revises: 
Create Date: 2026-09-16 14:01:03.953098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ba4934fdaa2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "incidents",
        sa.Column("incident_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("incident_type", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("severity", sa.String(), nullable=False, server_default="low"),
        sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")),
        sa.Column(
            "reported_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("incidents")
