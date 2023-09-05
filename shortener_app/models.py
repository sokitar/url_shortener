from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    shortened_url = Column(String, unique=True, index=True)
    target_url = Column(String, unique=True, index=True)
    hits = Column(Integer, default=0)
    created_on = Column(DateTime, default=func.now())
