from models.base_model import BaseModel
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.mysql import CHAR


class VcodeModel(BaseModel):
    __tablename__ = "vcode"
    vcode_id = Column(String(64), unique=True, comment="验证码ID")
    mobile = Column(CHAR(12), nullable=False, comment="手机号码")
    vcode = Column(CHAR(6), comment="验证码")
    type = Column(Integer, comment="验证码类型 0)注册 1)更新密码")
    expire_at = Column(DateTime, comment="验证码过期时间")
    status = Column(Integer, default=0, comment="验证码状态 0)待验证 1)已验证 2)已过期")

    def __init__(self, *args, **kwargs):
        super(VcodeModel, self).__init__(*args, **kwargs)
        self.vcode_id = self.uuid()
