"""init

Revision ID: b3073030bac7
Revises: 
Create Date: 2020-08-30 11:27:29.443435

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b3073030bac7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=False, comment='用户ID'),
    sa.Column('creator_id', sa.String(length=64), nullable=False, comment='创建者ID'),
    sa.Column('user_account', mysql.CHAR(length=12), nullable=False, comment='用户名'),
    sa.Column('user_mobile', mysql.CHAR(length=12), nullable=True, comment='手机号'),
    sa.Column('user_name', sa.String(length=64), nullable=True, comment='用户姓名'),
    sa.Column('level', sa.Integer(), nullable=False, comment='用户等级 9/root 可管理用户 1/read,write'),
    sa.Column('password', sa.String(length=128), nullable=True, comment='登录密码'),
    sa.Column('status', sa.Integer(), nullable=False, comment='用户状态 0=可使用，1=已注销'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_account'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('api_token',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True, comment='用户ID'),
    sa.Column('token_type', sa.String(length=32), nullable=True, comment='token类型 AccessToken/RefreshToken'),
    sa.Column('token', sa.String(length=128), nullable=True, comment='Token'),
    sa.Column('expire_at', sa.DateTime(), nullable=True, comment='Token过期时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('content', sa.Text(length=2048), nullable=True, comment='文章内容'),
    sa.Column('date', sa.String(length=128), nullable=True, comment='上线时间'),
    sa.Column('title', sa.String(length=128), nullable=True, comment='文章标题'),
    sa.Column('author', sa.String(length=128), nullable=True, comment='作者'),
    sa.Column('is_show', sa.Boolean(), nullable=True, comment='是否展示'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True, comment='姓名'),
    sa.Column('avatar', sa.String(length=128), nullable=True, comment='头像'),
    sa.Column('title1', sa.String(length=128), nullable=True, comment='抬头一'),
    sa.Column('title2', sa.String(length=128), nullable=True, comment='抬头一'),
    sa.Column('index', sa.Integer(), nullable=True, comment='顺序'),
    sa.Column('production', sa.Text(length=2048), nullable=True, comment='作品'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resource',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('video', sa.Text(length=2048), nullable=True, comment='视频代码'),
    sa.Column('video_cover_pic', sa.String(length=128), nullable=True, comment='视频封面'),
    sa.Column('full_pic', sa.String(length=128), nullable=True, comment='完整图片'),
    sa.Column('small_pic', sa.String(length=128), nullable=True, comment='缩略图'),
    sa.Column('info', sa.String(length=128), nullable=True, comment='视频介绍'),
    sa.Column('video_category', sa.String(length=64), nullable=True, comment='视频类别'),
    sa.Column('director', sa.String(length=12), nullable=True, comment='导演'),
    sa.Column('is_show', sa.Boolean(), nullable=True, comment='是否展示'),
    sa.Column('is_video', sa.Boolean(), nullable=True, comment='是否展示'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vcode',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('vcode_id', sa.String(length=64), nullable=True, comment='验证码ID'),
    sa.Column('mobile', mysql.CHAR(length=12), nullable=False, comment='手机号码'),
    sa.Column('vcode', mysql.CHAR(length=6), nullable=True, comment='验证码'),
    sa.Column('type', sa.Integer(), nullable=True, comment='验证码类型 0)注册 1)更新密码'),
    sa.Column('expire_at', sa.DateTime(), nullable=True, comment='验证码过期时间'),
    sa.Column('status', sa.Integer(), nullable=True, comment='验证码状态 0)待验证 1)已验证 2)已过期'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vcode_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vcode')
    op.drop_table('resource')
    op.drop_table('employee')
    op.drop_table('article')
    op.drop_table('api_token')
    op.drop_table('admin_user')
    # ### end Alembic commands ###
