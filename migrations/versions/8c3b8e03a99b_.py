"""empty message

Revision ID: 8c3b8e03a99b
Revises: f885399067be
Create Date: 2024-12-24 18:33:00.617636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c3b8e03a99b'
down_revision: Union[str, None] = 'f885399067be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('raw_transactions',
    sa.Column('transaction_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=38, scale=9), nullable=False),
    sa.Column('narration', sa.Text(), nullable=False),
    sa.Column('bank_account', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('raw_transactions')
    # ### end Alembic commands ###
