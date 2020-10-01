"""empty message

Revision ID: 8936f23d59f3
Revises: 1faf7a0db701
Create Date: 2020-07-02 10:24:06.934274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8936f23d59f3'
down_revision = '1faf7a0db701'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('hidden', sa.Boolean(create_constraint=False), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'hidden')
    # ### end Alembic commands ###
