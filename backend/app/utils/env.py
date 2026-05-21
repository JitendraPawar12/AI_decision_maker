import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    SERP_API_KEY: str
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    BACKEND_URL: str = "http://localhost:8000/api"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: Optional[Settings] = None


def load_environment() -> Settings:
    global settings
    load_dotenv()
    settings = Settings()
    return settings
