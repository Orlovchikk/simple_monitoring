from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    APP_URL: str
    CHECK_INTERVAL: int
    RESTART_COMMAND: str
    TIMEOUT: int
    RESTART_WAIT_TIME: int

    class Config:
        env_file = ".env"
