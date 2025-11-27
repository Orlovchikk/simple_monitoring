from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    APP_URL: str
    CHECK_INTERVAL: int
    LOG_FILE: str
    SERVICE_NAME: str
    RESTART_COMMAND: str
    TIMEOUT: int

    class Config:
        env_file = ".env"
