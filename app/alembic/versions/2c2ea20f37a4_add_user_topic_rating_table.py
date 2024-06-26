"""Add UserTopicRating table

Revision ID: 2c2ea20f37a4
Revises: b9629505f9b3
Create Date: 2024-05-31 23:17:31.171360

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2c2ea20f37a4'
down_revision = 'b9629505f9b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_topic_rating',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('rating',  sa.Integer(), nullable=False),
                    sa.Column('topic_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.bulk_insert(
        sa.table(
            'user_topic_rating',
            sa.column('id', sa.Integer),
            sa.column('user_id', sa.Integer),
            sa.column('rating', sa.Integer),
            sa.column('topic_id', sa.Integer)
        ),
        [
            {'id': 1, 'user_id': 1, 'rating': 1, 'topic_id': 1},
            {'id': 2, 'user_id': 2, 'rating': 2, 'topic_id': 2},
            {'id': 3, 'user_id': 3, 'rating': 3, 'topic_id': 3},
            {'id': 4, 'user_id': 4, 'rating': 5, 'topic_id': 2},
            {'id': 5, 'user_id': 4, 'rating': 3, 'topic_id': 3},
        ]
    )
    op.alter_column('schools', 'npsn',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('schools', 'school_name',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('schools', 'school_province',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('schools', 'school_city',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.drop_index('ix_schools_npsn', table_name='schools')
    op.alter_column('users', 'is_active',
                    existing_type=sa.BOOLEAN(),
                    nullable=False,
                    existing_server_default=sa.text('true'))
    op.alter_column('users', 'gender',
                    existing_type=postgresql.ENUM('male', 'female', name='gender_types'),
                    type_=sqlmodel.sql.sqltypes.AutoString(),
                    existing_nullable=True)
    op.drop_index('ix_user_email', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.drop_constraint('users_school_id_fkey1', 'users', type_='foreignkey')
    op.drop_constraint('users_school_major_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'class')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('class', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_school_major_id_fkey', 'users', 'school_major', ['school_major_id'], ['id'])
    op.create_foreign_key('users_school_id_fkey1', 'users', 'schools', ['school_id'], ['id'])
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_user_email', 'users', ['email'], unique=True)
    op.alter_column('users', 'gender',
                    existing_type=sqlmodel.sql.sqltypes.AutoString(),
                    type_=postgresql.ENUM('male', 'female', name='gender_types'),
                    existing_nullable=True)
    op.alter_column('users', 'is_active',
                    existing_type=sa.BOOLEAN(),
                    nullable=True,
                    existing_server_default=sa.text('true'))
    op.create_index('ix_schools_npsn', 'schools', ['npsn'], unique=True)
    op.alter_column('schools', 'school_city',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('schools', 'school_province',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('schools', 'school_name',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('schools', 'npsn',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.drop_table('user_topic_rating')
    # ### end Alembic commands ###
