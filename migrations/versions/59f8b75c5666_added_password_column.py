"""added password column

Revision ID: 59f8b75c5666
Revises: 4e961303a7b7
Create Date: 2025-02-03 13:01:13.357489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59f8b75c5666'
down_revision = '4e961303a7b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.TEXT(), nullable=True))
        batch_op.drop_column('hashed_password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashed_password', sa.TEXT(), nullable=True))
        batch_op.drop_column('password')

    # ### end Alembic commands ###
