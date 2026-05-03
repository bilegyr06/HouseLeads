"""add lead_matches table

Revision ID: e8c7f65ce775
Revises: 20260501_0001
Create Date: 2026-05-01 13:06:49.197707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8c7f65ce775'
down_revision: Union[str, None] = '20260501_0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This migration has been neutralized because `lead_matches` is already
    # created in the initial baseline revision. Keeping this revision file
    # present but as a no-op preserves history while avoiding duplicate DDL.
    return


def downgrade() -> None:
    # No-op downgrade to match neutralized upgrade above.
    return
