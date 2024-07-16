from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
from alembic import context

from .utils import config


@lru_cache
def get_settings():
    return config.Settings()

settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.db_dsn

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()