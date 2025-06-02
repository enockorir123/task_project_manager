"""Add users table and user_id to tasks

Revision ID: 2f25d887091f
Revises: d3256d8e731d
Create Date: 2025-06-02 23:41:05.575189

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2f25d887091f'
down_revision = 'd3256d8e731d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # 2. Use batch mode to add user_id column + named FK to tasks
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_tasks_user_id_users',  # explicit name for constraint
            'users',
            ['user_id'],
            ['id'],
            ondelete='SET NULL'
        )


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Drop the user_id foreign key and column with batch mode
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tasks_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    # 2. Drop users table and its index
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
