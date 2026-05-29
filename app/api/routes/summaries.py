from fastapi import APIRouter, Query
from datetime import date
from app.core.supabase import get_supabase
from app.services.ai_analyzer import analyze_daily_news

router = APIRouter()


@router.get("/")
def list_summaries(limit: int = Query(7, le=30)):
    db = get_supabase()
    summaries = db.table("daily_summaries").select("*, stock_picks(*)").order("date", desc=True).limit(limit).execute().data
    return summaries


@router.get("/today")
def today_summary():
    db = get_supabase()
    today = date.today().isoformat()
    result = db.table("daily_summaries").select("*, stock_picks(*)").eq("date", today).execute().data
    return result[0] if result else None


@router.post("/analyze")
async def trigger_analysis(analysis_date: date | None = None):
    result = await analyze_daily_news(analysis_date)
    return result
