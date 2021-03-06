"""add properties in news

Revision ID: 0a77c6ca5f97
Revises: 06f8ce358b54
Create Date: 2022-03-16 16:43:05.739497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a77c6ca5f97'
down_revision = '06f8ce358b54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('properties_news',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['new_id'], ['news.id'], name='property_new_new_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_new_property_id_foreign')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('properties_news')
    # ### end Alembic commands ###
