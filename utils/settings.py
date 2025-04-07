from celery import Celery
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class DataBaseSettings(BaseSettings):
    user: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASSWORD')
    host: str = Field(alias='DB_HOST')
    port: int = Field(alias='DB_PORT')
    database: str = Field(alias='DB_NAME')
    show_query: bool = Field(alias='DB_SHOW_QUERY', default=False)

    @property
    def async_dsn(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'

    @property
    def sync_dsn(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


class Settings(BaseSettings):
    db: DataBaseSettings = DataBaseSettings()


settings = Settings()


# celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")