from models.base_model import BaseModel
from sqlalchemy import Column, String, Text


class MessageModel(BaseModel):
    __tablename__ = "message"
    name = Column(String(128), comment="姓名")
    tel = Column(String(128), comment="联系方式")
    email = Column(String(128), comment="邮件")
    content = Column(Text(2048), comment="留言内容")

    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
