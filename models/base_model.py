import datetime
import uuid

from sqlalchemy import Column, BigInteger, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime)

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.created_at = datetime.datetime.now()
        self.update_at = datetime.datetime.now()

    @staticmethod
    def uuid():
        return uuid.uuid4().hex
