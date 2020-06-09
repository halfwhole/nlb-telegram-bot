"""Create book and availability tables

Revision ID: 104bc58ff196
Revises: 
Create Date: 2020-06-09 23:42:25.365287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '104bc58ff196'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'book',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('bid', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('title', sa.String(200)),
        sa.Column('author', sa.String(200))
    )
    op.create_table(
        'availability',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('book_id', sa.Integer, sa.ForeignKey('book.id'), nullable=False),
        sa.Column('branch_name', sa.String(200)),
        sa.Column('call_number', sa.String(200)),
        sa.Column('status_desc', sa.String(200)),
        sa.Column('shelf_location', sa.String(200))
    )


def downgrade():
    op.drop_table('availability')
    op.drop_table('book')
