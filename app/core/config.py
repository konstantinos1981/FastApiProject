from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # General project settings
    PROJECT_NAME: str = "Fast Api Project"
    DATABASE_URL: str = "sqlite://./test.db"
    SECRET_KEY: str = "Your_Secret_key"
    REFRESH_SECRET_KEY: str = "Refresh_Token_Secret_key"

    # JWT / Authentication settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

def get_settings() -> Settings:
    return Settings() 

settings = get_settings()  

