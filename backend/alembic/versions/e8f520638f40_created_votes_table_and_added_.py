"""Created votes table and added references to incidents and users table

Revision ID: e8f520638f40
Revises: 49603aad040f
Create Date: 2026-09-16 14:52:30.114986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8f520638f40'
down_revision: Union[str, Sequence[str], None] = '49603aad040f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('votes',
        sa.Column('vote_id', sa.Integer(), nullable=False),
        sa.Column('incident_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('vote_value', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.incident_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'],     ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('vote_id'),
        sa.UniqueConstraint('incident_id', 'user_id',   name='unique_user_incident_vote')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('votes')
