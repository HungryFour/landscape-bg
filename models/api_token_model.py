from sqlalchemy import Column, String, DateTime
from models.base_model import BaseModel


class ApiTokenModel(BaseModel):
    __tablename__ = "api_token"

    user_id = Column(String(64), comment="用户ID")
    token_type = Column(String(32), comment="token类型 AccessToken/RefreshToken")
    token = Column(String(128), comment="Token")
    expire_at = Column(DateTime, comment="Token过期时间")
