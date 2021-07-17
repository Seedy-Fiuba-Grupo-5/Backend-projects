"""seers_field

Revision ID: 2a067442affb
Revises: 2c6abac12b2b
Create Date: 2021-07-17 01:55:22.852276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a067442affb'
down_revision = '2c6abac12b2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('seer', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'seer')
    # ### end Alembic commands ###