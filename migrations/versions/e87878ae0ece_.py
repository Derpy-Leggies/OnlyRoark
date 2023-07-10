"""empty message

Revision ID: e87878ae0ece
Revises: 4cabe2b6cb85
Create Date: 2023-07-10 17:44:39.261088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e87878ae0ece'
down_revision = '4cabe2b6cb85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attachments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('original_file_name', sa.String(), nullable=True))
        batch_op.drop_column('otiginal_file_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attachments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('otiginal_file_name', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('original_file_name')

    # ### end Alembic commands ###