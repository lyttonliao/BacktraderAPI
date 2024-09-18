from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    CheckConstraint,
    UniqueConstraint,
    ARRAY,
    DateTime,
    JSON,
)
from datetime import datetime

from . import Base


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    public = Column(Boolean, nullable=False, index=True)
    inputs = Column(ARRAY(String))
    params = Column(JSON, nullable=False)
    user_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    version = Column(Integer, default=1)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="strategy_name_min_length"),
        CheckConstraint("LENGTH(name) <= 200", name="strategy_name_max_length"),
        UniqueConstraint("user_id", "name", name="uq_user_id_name"),
    )

    def __repr__(self):
        return f"<Strategy {self.name}>"
