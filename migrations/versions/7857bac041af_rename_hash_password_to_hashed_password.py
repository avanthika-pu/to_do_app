"""Rename hash_password to hashed_password

Revision ID: 7857bac041af
Revises: 65761a79bab8
Create Date: 2025-02-02 20:12:27.603841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7857bac041af'
down_revision = '65761a79bab8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashed_password', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('hashed_password')

    # ### end Alembic commands ###
