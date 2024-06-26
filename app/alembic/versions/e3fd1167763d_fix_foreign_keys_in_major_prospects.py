"""Fix foreign keys in major prospects

Revision ID: e3fd1167763d
Revises: faaac2c77696
Create Date: 2024-06-15 16:11:32.329227

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e3fd1167763d'
down_revision = 'faaac2c77696'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('prospect',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('prospect_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    #     sa.PrimaryKeyConstraint('id')
    # )
    op.create_foreign_key(None, 'major_course', 'major', ['major_id'], ['id'])
    op.create_foreign_key(None, 'major_course', 'course', ['course_id'], ['id'])
    op.create_foreign_key(None, 'major_prospect', 'major', ['major_id'], ['id'])
    op.create_foreign_key(None, 'major_prospect', 'future_prospect', ['prospect_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'major_prospect', type_='foreignkey')
    op.drop_constraint(None, 'major_prospect', type_='foreignkey')
    op.drop_constraint(None, 'major_course', type_='foreignkey')
    op.drop_constraint(None, 'major_course', type_='foreignkey')
    # op.drop_table('prospect')
    # ### end Alembic commands ###
