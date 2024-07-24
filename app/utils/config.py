from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    db_dsn: str
    db_max_open_conns: int = 25
    db_max_idle_conns: int = 25
    db_max_idle_time: str = "15m"
    algorithm: str
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings():
    settings = Settings()
    return settings


app_settings = get_settings()
