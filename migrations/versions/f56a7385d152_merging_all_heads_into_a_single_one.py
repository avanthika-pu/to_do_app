"""Merging all heads into a single one

Revision ID: f56a7385d152
Revises: 09bba0c4d681, 7fec46f2d5ef, 804ac9447c6c, 9e827e6be451, f465f36adeaa
Create Date: 2025-02-01 15:13:43.963959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f56a7385d152'
down_revision = ('09bba0c4d681', '7fec46f2d5ef', '804ac9447c6c', '9e827e6be451', 'f465f36adeaa')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
