from models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer


class EmployeeModel(BaseModel):
    __tablename__ = "employee"
    user_id = Column(String(64), nullable=False, unique=True, comment="用户ID")
    creator_id = Column(String(64), nullable=False,  comment="创建者用户ID")
    name = Column(String(128), comment="姓名")
    avatar = Column(String(128), comment="头像")
    title1 = Column(String(128), comment="抬头一")
    title2 = Column(String(128), comment="抬头一")
    index = Column(Integer, comment="顺序")
    production = Column(Text(2048), comment="作品")

    def __init__(self, *args, **kwargs):
        super(EmployeeModel, self).__init__(*args, **kwargs)
        self.user_id = self.uuid()
