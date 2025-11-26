"""Configuration settings for the orlwx application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openweathermap_api_key: str = ""
    orlando_lat: float = 28.5383
    orlando_lon: float = -81.3792


settings = Settings()
