"""empty message

Revision ID: 4cabe2b6cb85
Revises: d43011c17877
Create Date: 2023-07-10 17:44:16.632258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cabe2b6cb85'
down_revision = 'd43011c17877'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attachments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('otiginal_file_name', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('file_type', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('attachments')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.BOOLEAN(), nullable=True))

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('attachments', sa.BLOB(), nullable=True))

    op.drop_table('attachments')
    # ### end Alembic commands ###
