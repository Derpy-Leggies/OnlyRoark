"""empty message

Revision ID: 917950d1e40e
Revises: 5d35b342a76a
Create Date: 2023-07-10 05:57:24.541966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '917950d1e40e'
down_revision = '5d35b342a76a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
