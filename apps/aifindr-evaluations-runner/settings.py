import os
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    OPIK_URL_OVERRIDE: str = "http://host.docker.internal:5173/api"
    OPENAI_API_KEY: str = ""
    ELLMENTAL_API_URL: str = ""
    ELLMENTAL_API_KEY: str = ""
    
    @field_validator("*")
    def no_empty_strings(cls, v):
        if isinstance(v, str) and not v:
            raise ValueError("Field cannot be empty")
        return v
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra variables

class EnvSettings(BaseSettings):
    settings: Settings = Settings()

@lru_cache() # Cache settings to avoid re-reading the .env file on each call
def get_settings() -> Settings:
    if not os.getenv("SETTINGS"):
        return Settings()
    return EnvSettings().settings

settings = Settings()