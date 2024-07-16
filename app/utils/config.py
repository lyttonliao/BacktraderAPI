from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_dsn: str
    # db_max_open_conns: int = 25
    # db_max_idle_conns: int = 25
    # db_max_idle_time: str = "15m"
    

    model_config = SettingsConfigDict(env_file=".env")
