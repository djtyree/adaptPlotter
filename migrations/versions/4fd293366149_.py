"""empty message

Revision ID: 4fd293366149
Revises: None
Create Date: 2016-03-07 14:50:06.196000

"""

# revision identifiers, used by Alembic.
revision = '4fd293366149'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('speed', sa.Float(), nullable=True),
    sa.Column('dir', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('loc_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['loc_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jumppoint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('loc_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['loc_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rid', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('ip', sa.String(length=64), nullable=True),
    sa.Column('leader_id', sa.Integer(), nullable=True),
    sa.Column('loc_id', sa.Integer(), nullable=True),
    sa.Column('force_dir', sa.Float(), nullable=True),
    sa.Column('force_speed', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['leader_id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['loc_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('obstacle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('loc_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['loc_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('node_goal_association',
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goal.id'], ),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], )
    )
    op.create_table('node_jp_association',
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.Column('jumppoint_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['jumppoint_id'], ['jumppoint.id'], ),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('node_jp_association')
    op.drop_table('node_goal_association')
    op.drop_table('obstacle')
    op.drop_table('node')
    op.drop_table('jumppoint')
    op.drop_table('goal')
    op.drop_table('location')
    ### end Alembic commands ###
