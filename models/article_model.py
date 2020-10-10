from models.base_model import BaseModel
from sqlalchemy import Column, String, Boolean, Text


class ArticleModel(BaseModel):
    __tablename__ = "article"
    content = Column(Text(2048), comment="文章内容")
    date = Column(String(128), comment="上线时间")
    title = Column(String(128), comment="文章标题")
    pic = Column(String(256), comment="文章图片")
    author = Column(String(128), comment="作者")

    def __init__(self, *args, **kwargs):
        super(ArticleModel, self).__init__(*args, **kwargs)
