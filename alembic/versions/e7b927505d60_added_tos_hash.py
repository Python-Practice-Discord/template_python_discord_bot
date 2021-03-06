"""added tos hash

Revision ID: e7b927505d60
Revises: b04002e80f7d
Create Date: 2021-07-26 17:20:49.038414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7b927505d60'
down_revision = 'b04002e80f7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'bot_messages', ['name'])
    op.add_column('privacy_terms_of_service', sa.Column('hash', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('privacy_terms_of_service', 'hash')
    op.drop_constraint(None, 'bot_messages', type_='unique')
    # ### end Alembic commands ###
