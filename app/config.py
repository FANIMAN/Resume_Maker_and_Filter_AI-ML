# app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    postgres_db: str = Field(..., env="postgres_db")
    postgres_user: str = Field(..., env="postgres_user")
    postgres_password: str = Field(..., env="postgres_password")
    DATABASE_URL: str = Field(default=None, env="DATABASE_URL") 
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")



    class Config:
        env_file = ".env"
        extra = "forbid"  # explicitly forbid unknown environment variables


settings = Settings()


def get_settings():
    return settings


