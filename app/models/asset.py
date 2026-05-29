from pydantic import BaseModel
from enum import Enum


class AssetType(str, Enum):
    STOCK = "STOCK"
    FUND = "FUND"
    FOREX = "FOREX"


class SectorCode(str, Enum):
    # Stocks (SET)
    AGRO = "AGRO"
    CONSUMP = "CONSUMP"
    FINCIAL = "FINCIAL"
    INDUS = "INDUS"
    PROPCON = "PROPCON"
    RESOURC = "RESOURC"
    SERVICE = "SERVICE"
    TECH = "TECH"
    # Funds
    FUND_EQUITY = "FUND_EQUITY"
    FUND_FIXED = "FUND_FIXED"
    FUND_MIXED = "FUND_MIXED"
    FUND_REIT = "FUND_REIT"
    FUND_GLOBAL = "FUND_GLOBAL"
    FUND_MONEY = "FUND_MONEY"
    # Forex
    FX_MAJOR = "FX_MAJOR"
    FX_ASIA = "FX_ASIA"
    FX_COMMODITY = "FX_COMMODITY"


class AssetPrice(BaseModel):
    symbol: str
    asset_type: AssetType
    price: float
    change_1d: float
    change_pct_1d: float
    change_pct_1w: float | None = None
    change_pct_1m: float | None = None
    sparkline: list[float] = []


class Asset(BaseModel):
    id: str
    symbol: str
    name_th: str
    asset_type: AssetType
    sector_code: SectorCode | None = None
    metadata: dict = {}
