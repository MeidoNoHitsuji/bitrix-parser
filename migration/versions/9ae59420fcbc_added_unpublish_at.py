"""Added unpublish_at

Revision ID: 9ae59420fcbc
Revises: 84479467cb28
Create Date: 2022-04-19 15:47:55.866864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae59420fcbc'
down_revision = '84479467cb28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('catalog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('certificates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('computer_programs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('equipments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('faq', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('laboratories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('library_news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('patents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('phonebook', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('profkom_news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('trademarks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unpublished_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trademarks', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('profkom_news', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('phonebook', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('patents', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('library_news', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('laboratories', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('faq', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('equipments', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('computer_programs', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('certificates', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('catalog', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.drop_column('unpublished_at')

    # ### end Alembic commands ###
