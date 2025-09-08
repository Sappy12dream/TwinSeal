# app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    file_storage_path: str = Field(..., env="FILE_STORAGE_PATH")
    temp_id_expire_hours: int = Field(24, env="TEMP_ID_EXPIRE_HOURS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
