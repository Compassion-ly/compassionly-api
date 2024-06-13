"""relation for college & major

Revision ID: 4f7c4401127f
Revises: af4e1afa9f64
Create Date: 2024-06-12 20:56:15.711029

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '4f7c4401127f'
down_revision = 'af4e1afa9f64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('college', 'college_province')
    op.drop_column('college', 'college_city')
    op.add_column('college_detail', sa.Column('capacity', sa.Integer(), nullable=True))
    op.add_column('college_detail', sa.Column('interest', sa.Integer(), nullable=True))
    op.add_column('college_detail', sa.Column('portofolio_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.alter_column('college_detail', 'college_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('college_detail', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'college_detail', 'major', ['major_id'], ['id'])
    # ### end Alembic commands ###

    updates = [
        {"id": 1, "capacity": 100, "interest": 80, "portofolio_type": "Type A"},
        {"id": 2, "capacity": 120, "interest": 90, "portofolio_type": "Type B"},
        # Add more records as needed
    ]

    # Use the SQLAlchemy connection to perform updates
    conn = op.get_bind()
    for update in updates:
        conn.execute(
            sa.text(
                "UPDATE college_detail SET capacity = :capacity, interest = :interest, portofolio_type = :portofolio_type WHERE id = :id"
            ),
            {"id": update["id"], "capacity": update["capacity"], "interest": update["interest"], "portofolio_type": update["portofolio_type"]}
        )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'college_detail', type_='foreignkey')
    op.alter_column('college_detail', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('college_detail', 'college_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('college_detail', 'portofolio_type')
    op.drop_column('college_detail', 'interest')
    op.drop_column('college_detail', 'capacity')
    op.add_column('college', sa.Column('college_city', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('college', sa.Column('college_province', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###