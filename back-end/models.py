from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Weight(Base):
    __tablename__ = "weight"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Text)
    date = Column(DateTime)
