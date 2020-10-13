from models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Text


class ResourceModel(BaseModel):
    __tablename__ = "resource"
    video = Column(Text(2048), comment="视频代码")
    cover_pic = Column(String(128), comment="视频封面")
    title = Column(String(128), comment="标题")
    info = Column(String(128), comment="视频介绍")
    category = Column(String(64), comment="视频类别")
    director = Column(String(12), comment="导演")
    resource_type = Column(Integer, default=0, comment="0视频  1图片")

    def __init__(self, *args, **kwargs):
        super(ResourceModel, self).__init__(*args, **kwargs)
