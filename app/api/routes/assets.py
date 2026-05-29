from fastapi import APIRouter, Query
from app.core.supabase import get_supabase
from app.models.asset import AssetType
from app.services.price_service import get_stock_price, get_forex_price, get_fund_nav

router = APIRouter()


@router.get("/")
async def list_assets(
    asset_type: AssetType | None = Query(None),
    sector_code: str | None = Query(None),
):
    db = get_supabase()
    q = db.table("assets").select("*")
    if asset_type:
        q = q.eq("asset_type", asset_type)
    if sector_code:
        q = q.eq("sector_code", sector_code)
    return q.execute().data


@router.get("/{symbol}/price")
async def get_price(symbol: str, asset_type: AssetType):
    if asset_type == AssetType.STOCK:
        return await get_stock_price(symbol)
    elif asset_type == AssetType.FOREX:
        base, quote = symbol.split("/")
        return await get_forex_price(base, quote)
    else:
        return await get_fund_nav(symbol)
