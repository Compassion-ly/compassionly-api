"""Change column type of gender from enum to string to User model

Revision ID: e462a42a9a21
Revises: e29bd299cebe
Create Date: 2024-06-01 22:13:13.075975

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e462a42a9a21'
down_revision = 'e29bd299cebe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # alter table users change users.gender from enum type to string
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('gender',
                              type_=sa.String(),
                              existing_type=sa.Enum('male', 'female', name='gender_enum'),
                              existing_nullable=True)
        
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('gender',
                              type_=sa.Enum('male', 'female', name='gender_enum'),
                              existing_type=sa.String(),
                              existing_nullable=True)
    # ### end Alembic commands ###
