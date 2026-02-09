
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str

    # API keys
    read_api_key: str
    write_api_key: str

    # Retention
    retention_days: int = 30

    # Limits
    max_tags: int = 20
    max_tag_key_len: int = 50
    max_tag_value_len: int = 200
    max_page_size: int = 500

    # Logging
    log_level: str = "INFO"


settings = Settings()
