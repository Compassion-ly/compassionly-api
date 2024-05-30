"""Revisi modul user dan school

Revision ID: b9629505f9b3
Revises: e2412789c190
Create Date: 2024-05-30 19:48:50.574496

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = 'b9629505f9b3'
down_revision = 'e2412789c190'
branch_labels = None
depends_on = None


def upgrade():
    # Create school_major table
    op.create_table('school_major',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('school_major_name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    # Insert dummy data into school_major
    op.bulk_insert(
        sa.table(
            'school_major',
            sa.column('id', sa.Integer),
            sa.column('school_major_name', sa.String)
        ),
        [
            {'id': 1, 'school_major_name': 'MIPA'},
            {'id': 2, 'school_major_name': 'IPS'},
            {'id': 3, 'school_major_name': 'Bahasa'},
            {'id': 4, 'school_major_name': 'TKJ'},
            {'id': 5, 'school_major_name': 'RPL'}
        ]
    )

    # Modify users table to include new fields and correct relationships
    op.drop_column('users', 'user_schools_id')

    op.add_column('users', sa.Column('class', sa.Integer(), nullable=True))
    
    op.add_column('users', sa.Column('school_id', sa.Integer(), sa.ForeignKey('schools.id'), nullable=True))
    op.create_foreign_key(None, 'users', 'schools', ['school_id'], ['id'])

    # drop user_schools_id column and 
    op.add_column('users', sa.Column('school_major_id', sa.Integer(), sa.ForeignKey('school_major.id'), nullable=True))
    op.create_foreign_key(None, 'users', 'school_major', ['school_major_id'], ['id'])

    # drop the old user_schools table
    op.drop_table('user_schools')

    # reset seq
    op.execute("SELECT setval('school_major_id_seq', (SELECT max(id) FROM school_major))")

    # change the user of id 1 to have school_id 1, class 12, and school_major_id 1
    op.execute("UPDATE users SET school_id = 1, class = 12, school_major_id = 1 WHERE id = 1")


    # Insert additional dummy data into users

def downgrade():
    # reverse migration
    op.create_table('user_schools',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('school_id', sa.Integer(), nullable=True),
                    sa.Column('school_name', sa.String(), nullable=True),
                    sa.Column('school_major', sa.String(), nullable=True),
                    sa.Column('class', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    
    op.add_column('users', sa.Column('user_schools_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'user_schools', ['user_schools_id'], ['id'])


    op.drop_column('users', 'class')
    op.drop_column('users', 'school_id')
    op.drop_column('users', 'school_major_id')

    op.drop_table('school_major')

    op.execute("SELECT setval('user_schools_id_seq', (SELECT max(id) FROM user_schools))")
    op.execute("SELECT setval('users_id_seq', (SELECT max(id) FROM users))")
    op.execute("SELECT setval('school_major_id_seq', (SELECT max(id) FROM school_major))")
    

