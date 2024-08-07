"""Add description to MeetingRoom

Revision ID: da8b08f775fe
Revises: bfb22ae6ce67
Create Date: 2024-08-07 16:58:41.637876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da8b08f775fe'
down_revision: Union[str, None] = 'bfb22ae6ce67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meetingroom', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meetingroom', 'description')
    # ### end Alembic commands ###
