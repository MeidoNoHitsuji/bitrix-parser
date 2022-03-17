"""add value in templates

Revision ID: 93d92f6cc092
Revises: 0a77c6ca5f97
Create Date: 2022-03-16 16:56:19.682683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d92f6cc092'
down_revision = '0a77c6ca5f97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('templates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('key', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('templates', schema=None) as batch_op:
        batch_op.drop_column('key')

    # ### end Alembic commands ###
