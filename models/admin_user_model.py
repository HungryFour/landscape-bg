from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import CHAR
from models.base_model import BaseModel


class AdminUserModel(BaseModel):
    __tablename__ = "admin_user"

    user_id = Column(String(64), nullable=False, unique=True, comment="用户ID")
    creator_id = Column(String(64), nullable=False, comment="创建者ID")
    user_account = Column(CHAR(12), nullable=False, unique=True, comment="用户名")
    user_mobile = Column(CHAR(12), default=None, comment="手机号")
    user_name = Column(String(64), default=None, comment="用户姓名")
    level = Column(Integer, nullable=False, default=1, comment="用户等级 9/root 可管理用户 1/read,write")
    password = Column(String(128), default=None, comment="登录密码")
    status = Column(Integer, nullable=False, default=0, comment="用户状态 0=可使用，1=已注销")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = self.uuid()
