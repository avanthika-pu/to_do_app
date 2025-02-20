"""added archive field in the table

Revision ID: 7fec46f2d5ef
Revises: 9e827e6be451
Create Date: 2025-01-28 15:50:21.318759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fec46f2d5ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archived', sa.Boolean(), nullable=True))
        batch_op.drop_column('archeived')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archeived', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('archived')

    # ### end Alembic commands ###
