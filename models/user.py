from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from datetime import time

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(time)
    version = Column(Integer)

    strategies = relationship("strategy", back_populates="user")
