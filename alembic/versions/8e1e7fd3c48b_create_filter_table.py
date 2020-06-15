"""Create filter table

Revision ID: 8e1e7fd3c48b
Revises: 104bc58ff196
Create Date: 2020-06-15 21:01:38.854327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e1e7fd3c48b'
down_revision = '104bc58ff196'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'filter',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('branch_name', sa.String(200))
    )

def downgrade():
    op.drop_table('filter')
