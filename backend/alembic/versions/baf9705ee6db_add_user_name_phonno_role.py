"""Add user name, phonno, role

Revision ID: baf9705ee6db
Revises: e8f520638f40
Create Date: 2026-09-25 12:53:50.443983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'baf9705ee6db'
down_revision: Union[str, Sequence[str], None] = 'e8f520638f40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()
    user_role = sa.Enum("citizen", "responder", "admin", name="user_role")

    # A manually-created legacy enum may already exist with uppercase labels.
    # Do not let checkfirst silently reuse it: that makes the lowercase
    # server_default fail when PostgreSQL adds the column.
    enum_labels = bind.execute(
        sa.text(
            "SELECT e.enumlabel "
            "FROM pg_enum AS e "
            "JOIN pg_type AS t ON t.oid = e.enumtypid "
            "JOIN pg_namespace AS n ON n.oid = t.typnamespace "
            "WHERE t.typname = 'user_role' AND n.nspname = current_schema() "
            "ORDER BY e.enumsortorder"
        )
    ).scalars().all()

    if enum_labels and enum_labels != ["citizen", "responder", "admin"]:
        dependent_columns = bind.execute(
            sa.text(
                "SELECT n.nspname, c.relname, a.attname "
                "FROM pg_type AS t "
                "JOIN pg_namespace AS tn ON tn.oid = t.typnamespace "
                "JOIN pg_attribute AS a ON a.atttypid = t.oid "
                "JOIN pg_class AS c ON c.oid = a.attrelid "
                "JOIN pg_namespace AS n ON n.oid = c.relnamespace "
                "WHERE t.typname = 'user_role' "
                "AND tn.nspname = current_schema() "
                "AND a.attnum > 0 AND NOT a.attisdropped"
            )
        ).all()
        if dependent_columns:
            raise RuntimeError(
                "Found an incompatible user_role enum used by existing columns: "
                f"{dependent_columns}. Migrate those columns before retrying."
            )

        bind.execute(sa.text('DROP TYPE "user_role"'))

    user_role.create(bind, checkfirst=True)

    op.add_column(
        "users",
        sa.Column("user_fullname", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("user_phoneno", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column(
            "user_role",
            user_role,
            nullable=False,
            server_default="citizen",
        ),
    )

    # Preserve existing rows while adding required profile fields. Existing
    # users must update these placeholder values after the migration.
    op.execute(
        "UPDATE users SET user_fullname = 'Unknown', user_phoneno = '+910000000000' "
        "WHERE user_fullname IS NULL OR user_phoneno IS NULL"
    )
    op.alter_column("users", "user_fullname", nullable=False)
    op.alter_column("users", "user_phoneno", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "user_role")
    op.drop_column("users", "user_phoneno")
    op.drop_column("users", "user_fullname")
    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=True)
