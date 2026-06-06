import os
from dotenv import load_dotenv

load_dotenv()

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    app_name: str = "VakilAI"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    port: int = 8000

    secret_key: str = "test123"

    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "*"
    ]

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""

    anthropic_api_key: str = ""
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    bhashini_user_id: str = ""
    bhashini_api_key: str = ""
    bhashini_pipeline_id: str = ""

    max_file_size_mb: int = 50
    allowed_file_types: List[str] = ["pdf", "jpg", "jpeg", "png", "doc", "docx"]

    rate_limit_per_minute: int = 10
    free_tier_docs_per_month: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def ai_ready(self) -> bool:
        return bool(
            (self.anthropic_api_key and self.anthropic_api_key.startswith("sk-ant"))
            or
            (self.groq_api_key and self.groq_api_key.startswith("gsk_"))
        )

    @property
    def translation_ready(self) -> bool:
        return bool(self.bhashini_api_key and self.bhashini_user_id)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
