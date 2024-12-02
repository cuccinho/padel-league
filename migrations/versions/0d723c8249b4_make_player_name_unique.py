"""Make player name unique"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision = '0d723c8249b4'
down_revision = 'b0ecfc10bcc3'  # Replace with the previous migration's ID
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_players_name', ['name'])  # Name added: 'uq_players_name'


def downgrade():
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.drop_constraint('uq_players_name', type_='unique')
