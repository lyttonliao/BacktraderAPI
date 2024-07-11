from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import time

from ..database import Base

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    public = Column(Boolean, nullable=False, index=True)
    tags = Column(ARRAY(String), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(time)
    version = Column(Integer)

    user = relationship("User", back_populates="strategies")

    __table_args__ = (
        CheckConstraint('LENGTH(name) > 0', name='strategy_name_min_length'),
        CheckConstraint('LENGTH(name) <= 500', name='strategy_name_max_length'),
        UniqueConstraint('name', 'user_id', name='uq_strategy_name_user_id')
    )
