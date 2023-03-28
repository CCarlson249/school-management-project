"""initial data seed

Revision ID: d4ff7c12dc50
Revises: 726b1e4f4784
Create Date: 2023-03-27 17:13:54.751639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4ff7c12dc50'
down_revision = '726b1e4f4784'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grades', sa.Column('teachers_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'grades', type_='foreignkey')
    op.create_foreign_key(None, 'grades', 'teachers', ['teachers_id'], ['id'])
    op.drop_column('grades', 'teacher_id')
    op.add_column('students', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('students', sa.Column('last_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'last_name')
    op.drop_column('students', 'first_name')
    op.add_column('grades', sa.Column('teacher_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'grades', type_='foreignkey')
    op.create_foreign_key(None, 'grades', 'teachers', ['teacher_id'], ['id'])
    op.drop_column('grades', 'teachers_id')
    # ### end Alembic commands ###
