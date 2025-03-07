import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    OPIK_URL_OVERRIDE: str = "http://host.docker.internal:5173/api"
    OPENAI_API_KEY: str = ""
    ELLMENTAL_API_URL: str = ""
    ELLMENTAL_API_KEY: str = ""


class EnvSettings(BaseSettings):
    settings: Settings = Settings()


@lru_cache()  # Cache settings to avoid re-reading the .env file on each call
def get_settings() -> Settings:
    if not os.getenv("SETTINGS"):
        return Settings()
    return EnvSettings().settings


settings = get_settings()
