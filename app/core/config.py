from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str
    supabase_key: str
    anthropic_api_key: str
    cors_origins: list[str] = ["http://localhost:3000"]

    # News sources (RSS)
    news_sources: list[str] = [
        "https://www.bangkokpost.com/rss/data/business.xml",
        "https://feeds.reuters.com/reuters/businessNews",
    ]

    # Scheduler
    news_fetch_hour: int = 6
    analysis_hour: int = 7


settings = Settings()
