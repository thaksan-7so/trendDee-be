import feedparser
import httpx
from datetime import datetime, timezone
from app.core.config import settings
from app.core.supabase import get_supabase


async def fetch_all_news() -> list[dict]:
    articles = []
    for url in settings.news_sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                articles.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "source": feed.feed.get("title", url),
                    "content": entry.get("summary", ""),
                    "published_at": _parse_date(entry),
                    "sector_codes": [],
                    "ticker_mentions": [],
                })
        except Exception as e:
            print(f"[news_fetcher] Failed {url}: {e}")

    return articles


def _parse_date(entry) -> str:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return dt.isoformat()
    return datetime.now(timezone.utc).isoformat()


async def save_articles(articles: list[dict]):
    db = get_supabase()
    if not articles:
        return
    db.table("news_articles").upsert(articles, on_conflict="url").execute()
    print(f"[news_fetcher] Saved {len(articles)} articles")
