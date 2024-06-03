"""add module topics

Revision ID: ec76d464675a
Revises: 5f053c4e8c2d
Create Date: 2024-06-03 22:03:38.059912

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'ec76d464675a'
down_revision = '5f053c4e8c2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('topics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('topic_category_id', sa.Integer(), nullable=True),
    sa.Column('short_introduction', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('topic_image', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('topic_image2', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('topic_explanation', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.bulk_insert(
        sa.table(
            'topics',
            sa.column('id', sa.Integer),
            sa.column('topic_name', sa.String),
            sa.column('topic_category_id', sa.Integer),
            sa.column('short_introduction', sa.String),
            sa.column('topic_image', sa.String),
            sa.column('topic_image2', sa.String),
            sa.column('topic_explanation', sa.String)
        ),
        [
            {'topic_name': 'Topic 1', 'topic_category_id': 1, 'short_introduction': 'Introduction to Topic 1', 'topic_image': 'https://example.com/image1.jpg', 'topic_image2': 'https://example.com/image2.jpg', 'topic_explanation': 'Explanation of Topic 1'},
            {'topic_name': 'Topic 2', 'topic_category_id': 2, 'short_introduction': 'Introduction to Topic 2', 'topic_image': 'https://example.com/image3.jpg', 'topic_image2': 'https://example.com/image4.jpg', 'topic_explanation': 'Explanation of Topic 2'},
            {'topic_name': 'Topic 3', 'topic_category_id': 3, 'short_introduction': 'Introduction to Topic 3', 'topic_image': 'https://example.com/image5.jpg', 'topic_image2': 'https://example.com/image6.jpg', 'topic_explanation': 'Explanation of Topic 3'}
        ]
    )
    op.add_column('college', sa.Column('college_province', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('college', sa.Column('college_city', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_column('college', 'college_type_name')
    op.alter_column('college_detail', 'college_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('college_detail', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('college_detail_major_id_fkey', 'college_detail', type_='foreignkey')
    op.alter_column('course', 'course_image',
               existing_type=sa.TEXT(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.alter_column('course', 'course_definition',
               existing_type=sa.TEXT(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.alter_column('course', 'course_explain',
               existing_type=sa.TEXT(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.alter_column('future_prospect', 'description',
               existing_type=sa.TEXT(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.alter_column('major', 'major_definition',
               existing_type=sa.TEXT(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.alter_column('major', 'major_image',
               existing_type=sa.TEXT(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.alter_column('major_course', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('major_course', 'course_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('major_course_course_id_fkey', 'major_course', type_='foreignkey')
    op.drop_constraint('major_course_major_id_fkey', 'major_course', type_='foreignkey')
    op.alter_column('major_personality', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('major_personality', 'personality_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('major_personality_major_id_fkey', 'major_personality', type_='foreignkey')
    op.drop_constraint('major_personality_personality_id_fkey', 'major_personality', type_='foreignkey')
    op.alter_column('major_prospect', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('major_prospect', 'prospect_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('major_prospect_major_id_fkey', 'major_prospect', type_='foreignkey')
    op.drop_constraint('major_prospect_prospect_id_fkey', 'major_prospect', type_='foreignkey')
    op.alter_column('user_topic_rating', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user_topic_rating', 'rating',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('user_topic_rating_user_id_fkey', 'user_topic_rating', type_='foreignkey')
    op.drop_constraint('users_school_major_id_fkey1', 'users', type_='foreignkey')
    op.drop_constraint('users_school_id_fkey', 'users', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('users_school_id_fkey', 'users', 'schools', ['school_id'], ['id'])
    op.create_foreign_key('users_school_major_id_fkey1', 'users', 'school_major', ['school_major_id'], ['id'])
    op.create_foreign_key('user_topic_rating_user_id_fkey', 'user_topic_rating', 'users', ['user_id'], ['id'])
    op.alter_column('user_topic_rating', 'rating',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user_topic_rating', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key('major_prospect_prospect_id_fkey', 'major_prospect', 'future_prospect', ['prospect_id'], ['id'])
    op.create_foreign_key('major_prospect_major_id_fkey', 'major_prospect', 'major', ['major_id'], ['id'])
    op.alter_column('major_prospect', 'prospect_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('major_prospect', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key('major_personality_personality_id_fkey', 'major_personality', 'personality', ['personality_id'], ['id'])
    op.create_foreign_key('major_personality_major_id_fkey', 'major_personality', 'major', ['major_id'], ['id'])
    op.alter_column('major_personality', 'personality_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('major_personality', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key('major_course_major_id_fkey', 'major_course', 'major', ['major_id'], ['id'])
    op.create_foreign_key('major_course_course_id_fkey', 'major_course', 'course', ['course_id'], ['id'])
    op.alter_column('major_course', 'course_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('major_course', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('major', 'major_image',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('major', 'major_definition',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('future_prospect', 'description',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('course', 'course_explain',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('course', 'course_definition',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('course', 'course_image',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.create_foreign_key('college_detail_major_id_fkey', 'college_detail', 'major', ['major_id'], ['id'])
    op.alter_column('college_detail', 'major_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('college_detail', 'college_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('college', sa.Column('college_type_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('college', 'college_city')
    op.drop_column('college', 'college_province')
    op.drop_table('topics')
    # ### end Alembic commands ###
