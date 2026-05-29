import yfinance as yf
import httpx
from app.models.asset import AssetPrice, AssetType


async def get_stock_price(symbol: str) -> AssetPrice:
    ticker = yf.Ticker(f"{symbol}.BK")  # .BK = SET suffix
    hist = ticker.history(period="1mo")

    current = float(hist["Close"].iloc[-1])
    prev_day = float(hist["Close"].iloc[-2])
    prev_week = float(hist["Close"].iloc[-6]) if len(hist) >= 6 else prev_day
    prev_month = float(hist["Close"].iloc[0])

    sparkline = hist["Close"].tail(7).tolist()

    return AssetPrice(
        symbol=symbol,
        asset_type=AssetType.STOCK,
        price=current,
        change_1d=current - prev_day,
        change_pct_1d=(current - prev_day) / prev_day * 100,
        change_pct_1w=(current - prev_week) / prev_week * 100,
        change_pct_1m=(current - prev_month) / prev_month * 100,
        sparkline=sparkline,
    )


async def get_forex_price(base: str, quote: str) -> AssetPrice:
    symbol = f"{base}{quote}=X"
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo")

    current = float(hist["Close"].iloc[-1])
    prev_day = float(hist["Close"].iloc[-2])
    prev_week = float(hist["Close"].iloc[-6]) if len(hist) >= 6 else prev_day
    prev_month = float(hist["Close"].iloc[0])

    sparkline = hist["Close"].tail(7).tolist()

    return AssetPrice(
        symbol=f"{base}/{quote}",
        asset_type=AssetType.FOREX,
        price=current,
        change_1d=current - prev_day,
        change_pct_1d=(current - prev_day) / prev_day * 100,
        change_pct_1w=(current - prev_week) / prev_week * 100,
        change_pct_1m=(current - prev_month) / prev_month * 100,
        sparkline=sparkline,
    )


async def get_fund_nav(fund_code: str) -> AssetPrice:
    # SEC Thailand public API
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.sec.or.th/FundFactsheet/fund/dailynav/{fund_code}",
            headers={"accept": "application/json"},
        )
        data = resp.json()

    nav_list = data.get("data", [])
    if not nav_list:
        raise ValueError(f"No NAV data for {fund_code}")

    current = float(nav_list[0]["nav"])
    prev = float(nav_list[1]["nav"]) if len(nav_list) > 1 else current
    sparkline = [float(d["nav"]) for d in reversed(nav_list[:7])]

    return AssetPrice(
        symbol=fund_code,
        asset_type=AssetType.FUND,
        price=current,
        change_1d=current - prev,
        change_pct_1d=(current - prev) / prev * 100,
        sparkline=sparkline,
    )
