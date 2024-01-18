"""streams and schedules

Revision ID: 085c0f67d82b
Revises: c00536c427b9
Create Date: 2024-01-16 13:09:28.541985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '085c0f67d82b'
down_revision = 'c00536c427b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True, comment='title for the stream'),
    sa.Column('day_of_week', sa.Integer(), nullable=False, comment='day of week the stream will run on'),
    sa.Column('start_time', sa.Integer(), nullable=False, comment='time of day that the stream should start'),
    sa.Column('end_time', sa.Integer(), nullable=False, comment='time of day that the stream should end'),
    sa.Column('repeat_until', sa.Integer(), nullable=True, comment='timestamp: if the stream should stop after a certain date'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stream',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('ip_address', sa.Integer(), nullable=False),
    sa.Column('api', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip_address'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stream_schedule',
    sa.Column('stream_id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.ForeignKeyConstraint(['stream_id'], ['stream.id'], ),
    sa.PrimaryKeyConstraint('stream_id', 'schedule_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stream_schedule')
    op.drop_table('stream')
    op.drop_table('schedule')
    # ### end Alembic commands ###
