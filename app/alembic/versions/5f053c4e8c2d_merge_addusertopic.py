"""Merge addusertopic

Revision ID: 5f053c4e8c2d
Revises: e462a42a9a21, 2c2ea20f37a4
Create Date: 2024-06-03 20:04:06.612699

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '5f053c4e8c2d'
down_revision = ('e462a42a9a21', '2c2ea20f37a4')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
