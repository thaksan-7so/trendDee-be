from app.core.supabase import get_supabase
from app.models.portfolio import Position, PositionStatus, PortfolioSummary
from app.services.price_service import get_stock_price, get_forex_price, get_fund_nav
from app.models.asset import AssetType


def _get_status(pnl_pct: float, ai_signal: str) -> PositionStatus:
    is_profit = pnl_pct >= 0
    signal = ai_signal.lower()

    if not is_profit and signal == "sell":
        return PositionStatus.DANGER_SELL
    if not is_profit and signal in ("hold", "buy"):
        return PositionStatus.DOI
    if is_profit and signal == "sell":
        return PositionStatus.SELL_PROFIT
    return PositionStatus.HOLD


async def get_portfolio_summary() -> PortfolioSummary:
    db = get_supabase()

    txns = db.table("portfolio_transactions").select("*").execute().data
    picks = db.table("stock_picks").select("*").order("date", desc=True).limit(50).execute().data
    ai_signals = {p["ticker"]: p for p in picks}

    # Aggregate positions
    holdings: dict[str, dict] = {}
    for t in txns:
        key = t["asset_id"]
        if key not in holdings:
            holdings[key] = {
                "asset_id": t["asset_id"],
                "symbol": t["symbol"],
                "name_th": t.get("name_th", t["symbol"]),
                "asset_type": t["asset_type"],
                "sector_code": t.get("sector_code"),
                "quantity": 0.0,
                "total_cost": 0.0,
            }
        if t["action"] == "buy":
            holdings[key]["quantity"] += t["quantity"]
            holdings[key]["total_cost"] += t["quantity"] * t["price"]
        else:
            holdings[key]["quantity"] -= t["quantity"]

    positions = []
    total_value = 0.0
    total_cost = 0.0

    for h in holdings.values():
        if h["quantity"] <= 0:
            continue

        asset_type = AssetType(h["asset_type"])
        try:
            if asset_type == AssetType.STOCK:
                price_data = await get_stock_price(h["symbol"])
            elif asset_type == AssetType.FOREX:
                base, quote = h["symbol"].split("/")
                price_data = await get_forex_price(base, quote)
            else:
                price_data = await get_fund_nav(h["symbol"])
            current_price = price_data.price
        except Exception:
            current_price = h["total_cost"] / h["quantity"]

        avg_cost = h["total_cost"] / h["quantity"]
        cost_basis = h["quantity"] * avg_cost
        current_value = h["quantity"] * current_price
        pnl = current_value - cost_basis
        pnl_pct = pnl / cost_basis * 100

        signal_data = ai_signals.get(h["symbol"], {})
        ai_signal = signal_data.get("action", "hold")
        ai_reasoning = signal_data.get("reasoning", "ยังไม่มีการวิเคราะห์")

        positions.append(Position(
            asset_id=h["asset_id"],
            symbol=h["symbol"],
            name_th=h["name_th"],
            asset_type=asset_type,
            sector_code=h.get("sector_code"),
            quantity=h["quantity"],
            avg_cost=avg_cost,
            current_price=current_price,
            cost_basis=cost_basis,
            current_value=current_value,
            pnl=pnl,
            pnl_pct=pnl_pct,
            status=_get_status(pnl_pct, ai_signal),
            ai_signal=ai_signal,
            ai_reasoning=ai_reasoning,
        ))

        total_value += current_value
        total_cost += cost_basis

    allocation_by_type: dict[str, float] = {}
    allocation_by_sector: dict[str, float] = {}
    for p in positions:
        allocation_by_type[p.asset_type] = allocation_by_type.get(p.asset_type, 0) + p.current_value
        if p.sector_code:
            allocation_by_sector[p.sector_code] = allocation_by_sector.get(p.sector_code, 0) + p.current_value

    return PortfolioSummary(
        total_value=total_value,
        total_cost=total_cost,
        total_pnl=total_value - total_cost,
        total_pnl_pct=(total_value - total_cost) / total_cost * 100 if total_cost else 0,
        positions=positions,
        allocation_by_type={k: v / total_value * 100 for k, v in allocation_by_type.items()},
        allocation_by_sector={k: v / total_value * 100 for k, v in allocation_by_sector.items()},
    )
