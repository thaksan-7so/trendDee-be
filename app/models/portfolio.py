from pydantic import BaseModel
from datetime import date
from enum import Enum
from app.models.asset import AssetType


class TradeAction(str, Enum):
    BUY = "buy"
    SELL = "sell"


class PositionStatus(str, Enum):
    HOLD = "ถือต่อ"
    SELL_PROFIT = "ขายทำกำไร"
    DANGER_SELL = "ควรรีบขาย"
    DOI = "ดอย"


class TransactionCreate(BaseModel):
    asset_id: str
    asset_type: AssetType
    action: TradeAction
    quantity: float
    price: float
    transaction_date: date
    notes: str | None = None


class Transaction(TransactionCreate):
    id: str


class Position(BaseModel):
    asset_id: str
    symbol: str
    name_th: str
    asset_type: AssetType
    sector_code: str | None
    quantity: float
    avg_cost: float
    current_price: float
    cost_basis: float
    current_value: float
    pnl: float
    pnl_pct: float
    status: PositionStatus
    ai_signal: str
    ai_reasoning: str


class PortfolioSummary(BaseModel):
    total_value: float
    total_cost: float
    total_pnl: float
    total_pnl_pct: float
    positions: list[Position]
    allocation_by_type: dict[str, float]
    allocation_by_sector: dict[str, float]
