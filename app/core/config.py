from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    DATABASE_URL: str
    API_KEY: str
    GOOGLE_SERVICE_ACCOUNT_FILE: str  
    GOOGLE_CALENDAR_ID: str 
    SCOPES: str

settings = Settings() 