from fastapi import APIRouter, Query
from app.core.supabase import get_supabase
from app.services.news_fetcher import fetch_all_news, save_articles

router = APIRouter()


@router.get("/")
def list_news(
    sector_code: str | None = Query(None),
    limit: int = Query(20, le=100),
):
    db = get_supabase()
    q = db.table("news_articles").select("*").order("published_at", desc=True).limit(limit)
    if sector_code:
        q = q.contains("sector_codes", [sector_code])
    return q.execute().data


@router.post("/fetch")
async def trigger_fetch():
    articles = await fetch_all_news()
    await save_articles(articles)
    return {"fetched": len(articles)}
