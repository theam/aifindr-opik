import os
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    OPIK_URL_OVERRIDE: str = "http://host.docker.internal:5173/api"
    OPENAI_API_KEY: str = ""
    
    @field_validator("*")
    def no_empty_strings(cls, v):
        if isinstance(v, str) and not v:
            raise ValueError(f"Field {v} cannot be empty")
        return v
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Permite ignorar variables extra

settings = Settings()

print("Settings: ", settings)