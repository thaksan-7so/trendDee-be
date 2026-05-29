from pydantic import BaseModel
from datetime import datetime


class NewsArticle(BaseModel):
    id: str
    title: str
    url: str
    source: str
    content: str | None = None
    published_at: datetime
    sector_codes: list[str] = []
    ticker_mentions: list[str] = []


class DailySummary(BaseModel):
    id: str
    date: str
    summary_text: str
    market_sentiment: str  # bullish | bearish | neutral
    stock_picks: list["StockPick"]


class StockPick(BaseModel):
    ticker: str
    name_th: str | None = None
    asset_type: str
    sector_code: str | None = None
    action: str  # buy | hold | sell
    reasoning: str
    confidence: float
