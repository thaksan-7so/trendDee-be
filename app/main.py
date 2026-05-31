import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import assets, portfolio, news, summaries

# APScheduler ทำงานได้เฉพาะ long-running server (Render/local)
# บน Vercel (serverless) ใช้ Vercel Cron แทน
USE_SCHEDULER = os.getenv("USE_SCHEDULER", "false").lower() == "true"

if USE_SCHEDULER:
    from app.schedulers.jobs import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    if USE_SCHEDULER:
        start_scheduler()
    yield
    if USE_SCHEDULER:
        stop_scheduler()


app = FastAPI(
    title="TrendDee API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router, prefix="/api/assets", tags=["assets"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(summaries.router, prefix="/api/summaries", tags=["summaries"])


@app.get("/health")
def health():
    return {"status": "ok"}
