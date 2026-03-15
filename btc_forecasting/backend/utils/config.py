from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    MLFLOW_TRACKING_URI: str = Field(default="http://localhost:5000", env="MLFLOW_TRACKING_URI")
    BINANCE_API_KEY: Optional[str] = Field(None, env="BINANCE_API_KEY")
    BINANCE_SECRET: Optional[str] = Field(None, env="BINANCE_SECRET")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

