import json
import anthropic
from datetime import date
from app.core.config import settings
from app.core.supabase import get_supabase

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

SECTORS = "AGRO, CONSUMP, FINCIAL, INDUS, PROPCON, RESOURC, SERVICE, TECH, FUND_EQUITY, FUND_FIXED, FUND_REIT, FUND_GLOBAL, FX_MAJOR, FX_ASIA"


async def analyze_daily_news(news_date: date | None = None) -> dict:
    db = get_supabase()
    today = (news_date or date.today()).isoformat()

    rows = (
        db.table("news_articles")
        .select("title, content, source")
        .gte("published_at", f"{today}T00:00:00")
        .lte("published_at", f"{today}T23:59:59")
        .limit(30)
        .execute()
    )

    if not rows.data:
        return {}

    news_text = "\n\n".join(
        f"[{r['source']}] {r['title']}\n{r.get('content', '')[:300]}"
        for r in rows.data
    )

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""วิเคราะห์ข่าวการลงทุนต่อไปนี้ แล้วตอบเป็น JSON:

{news_text}

ตอบในรูปแบบ JSON เท่านั้น (ไม่ต้องมีข้อความอื่น):
{{
  "summary": "สรุปภาพรวมตลาดวันนี้ 2-3 ประโยค",
  "sentiment": "bullish | bearish | neutral",
  "picks": [
    {{
      "ticker": "ADVANC",
      "asset_type": "STOCK | FUND | FOREX",
      "sector_code": "TECH",
      "action": "buy | hold | sell",
      "reasoning": "เหตุผล 1-2 ประโยค",
      "confidence": 0.85
    }}
  ]
}}

กลุ่มที่เลือกได้: {SECTORS}
แนะนำไม่เกิน 5 รายการ""",
        }],
    )

    result = json.loads(response.content[0].text)
    result["date"] = today

    db.table("daily_summaries").upsert(
        {"date": today, "summary_text": result["summary"], "market_sentiment": result["sentiment"]},
        on_conflict="date",
    ).execute()

    if result.get("picks"):
        db.table("stock_picks").delete().eq("date", today).execute()
        db.table("stock_picks").insert([
            {**pick, "date": today} for pick in result["picks"]
        ]).execute()

    return result


async def classify_news_sectors(article_id: str, title: str, content: str) -> list[str]:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""ข่าว: {title}\n{content[:500]}

ระบุกลุ่มอุตสาหกรรมที่เกี่ยวข้อง (ตอบเป็น JSON array เท่านั้น):
เช่น ["TECH", "FINCIAL"]

กลุ่มที่เลือกได้: {SECTORS}""",
        }],
    )

    sectors = json.loads(response.content[0].text)
    db = get_supabase()
    db.table("news_articles").update({"sector_codes": sectors}).eq("id", article_id).execute()
    return sectors
