from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


CURRENT_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    
    DEBUG: bool
    SECRET_KEY: str

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    
    model_config = SettingsConfigDict(
        
        env_file=[
            CURRENT_DIR / "../../.env",  
            ".env",                      
        ],
        env_file_encoding="utf-8",
        extra="ignore",                 
    )


settings = Settings()
