from sqlalchemy import Boolean, Column, Integer, String, CheckConstraint, UniqueConstraint, ARRAY, DateTime
from datetime import datetime

from . import Base


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    public = Column(Boolean, nullable=False, index=True)
    tags = Column(ARRAY(String), index=True)
    user_id = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    version = Column(Integer)

    __table_args__ = (
        CheckConstraint('LENGTH(name) > 0', name='strategy_name_min_length'),
        CheckConstraint('LENGTH(name) <= 200', name='strategy_name_max_length'),
        UniqueConstraint('name', 'user_id', name='uq_strategy_name_user_id')
    )

    def __repr__(self):
        return f"<Strategy {self.name}>"