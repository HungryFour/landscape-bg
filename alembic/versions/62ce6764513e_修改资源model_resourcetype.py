"""修改资源model resourceType

Revision ID: 62ce6764513e
Revises: 287ec0e989fe
Create Date: 2020-10-13 11:57:02.141208

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '62ce6764513e'
down_revision = '287ec0e989fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('resource_type', sa.Integer(), nullable=True, comment='0视频  1图片'))
    op.drop_column('resource', 'is_video')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('is_video', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否是视频'))
    op.drop_column('resource', 'resource_type')
    # ### end Alembic commands ###
