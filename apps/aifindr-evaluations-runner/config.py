import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPIK_URL: str = os.getenv("OPIK_URL", "http://host.docker.internal:5173/api")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings() 