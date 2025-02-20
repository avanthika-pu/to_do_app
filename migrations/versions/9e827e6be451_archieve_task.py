"""archieve task

Revision ID: 9e827e6be451
Revises: 804ac9447c6c
Create Date: 2025-01-27 17:09:18.875011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e827e6be451'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archeived', sa.Boolean(), nullable=True))
        batch_op.drop_column('archived')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archived', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('archeived')

    # ### end Alembic commands ###
