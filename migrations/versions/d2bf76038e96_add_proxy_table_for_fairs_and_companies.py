"""Add proxy table for Fairs and Companies

Revision ID: d2bf76038e96
Revises: 2cb6b12db4a3
Create Date: 2023-09-27 12:40:02.558234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2bf76038e96'
down_revision: Union[str, None] = '2cb6b12db4a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fair_proxy',
    sa.Column('status', sa.Enum('SENT', 'ACCEPTED', 'REJECTED', name='fairproxystatus'), nullable=False),
    sa.Column('invitation', sa.Boolean(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('fair_id', sa.Integer(), nullable=False),
    sa.Column('stall_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['fair_id'], ['fair.id'], ),
    sa.ForeignKeyConstraint(['stall_id'], ['stall.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('company_id', 'fair_id')
    )
    # op.create_index('proxy_index', 'fair_proxy', ['company_id', 'fair_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fair_proxy')
    # ### end Alembic commands ###
