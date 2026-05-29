import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.config import settings

scheduler = BackgroundScheduler()


def _run_async(coro):
    asyncio.run(coro)


def _fetch_news_job():
    from app.services.news_fetcher import fetch_all_news, save_articles
    async def run():
        articles = await fetch_all_news()
        await save_articles(articles)
    _run_async(run())


def _analyze_job():
    from app.services.ai_analyzer import analyze_daily_news
    _run_async(analyze_daily_news())


def start_scheduler():
    scheduler.add_job(_fetch_news_job, "cron", hour=settings.news_fetch_hour, minute=0)
    scheduler.add_job(_analyze_job, "cron", hour=settings.analysis_hour, minute=0)
    scheduler.start()
    print("[scheduler] Started — news fetch at 06:00, analysis at 07:00")


def stop_scheduler():
    scheduler.shutdown()
