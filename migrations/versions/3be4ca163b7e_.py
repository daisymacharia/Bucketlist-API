"""empty message

Revision ID: 3be4ca163b7e
Revises: 9d7f5d19efb6
Create Date: 2017-07-01 22:13:26.748738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3be4ca163b7e'
down_revision = '9d7f5d19efb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fullnames', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'fullnames')
    # ### end Alembic commands ###
