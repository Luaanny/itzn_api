from pydantic import BaseSettings, BaseSettingsDict

class Settings(BaseSettings):
    model_config = BaseSettingsDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    DATABASE_URL: str
    SECRET_KEY: str

settings = Settings()
