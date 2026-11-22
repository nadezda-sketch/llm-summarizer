from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    llm_api_key: str = "MISSING"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_timeout_seconds: float = 10.0
    llm_max_retries: int = 2

    app_env: str = "dev"
    log_level: str = "INFO"
    max_input_chars: int = 12000
    default_max_sentences: int = 3

    cache_ttl_seconds: int = 300
    cache_max_size: int = 512

settings = Settings()