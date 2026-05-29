"""
Seed initial assets: หุ้น SET, กองทุน, Forex
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.supabase import get_supabase

STOCKS = [
    {"symbol": "ADVANC",  "name_th": "แอดวานซ์ อินโฟร์ เซอร์วิส",  "sector_code": "TECH"},
    {"symbol": "INTUCH",  "name_th": "อินทัช โฮลดิ้งส์",            "sector_code": "TECH"},
    {"symbol": "TRUE",    "name_th": "ทรู คอร์ปอเรชั่น",            "sector_code": "TECH"},
    {"symbol": "PTT",     "name_th": "ปตท.",                         "sector_code": "RESOURC"},
    {"symbol": "PTTEP",   "name_th": "ปตท. สำรวจและผลิตปิโตรเลียม", "sector_code": "RESOURC"},
    {"symbol": "KBANK",   "name_th": "กสิกรไทย",                    "sector_code": "FINCIAL"},
    {"symbol": "SCB",     "name_th": "ไทยพาณิชย์",                  "sector_code": "FINCIAL"},
    {"symbol": "BBL",     "name_th": "กรุงเทพ",                     "sector_code": "FINCIAL"},
    {"symbol": "KTB",     "name_th": "กรุงไทย",                     "sector_code": "FINCIAL"},
    {"symbol": "CPF",     "name_th": "เจริญโภคภัณฑ์อาหาร",          "sector_code": "AGRO"},
    {"symbol": "TU",      "name_th": "ไทยยูเนี่ยน กรุ๊ป",           "sector_code": "AGRO"},
    {"symbol": "MINT",    "name_th": "ไมเนอร์ อินเตอร์เนชั่นแนล",   "sector_code": "SERVICE"},
    {"symbol": "AOT",     "name_th": "ท่าอากาศยานไทย",              "sector_code": "SERVICE"},
    {"symbol": "CPN",     "name_th": "เซ็นทรัลพัฒนา",              "sector_code": "PROPCON"},
    {"symbol": "SCC",     "name_th": "ปูนซิเมนต์ไทย",              "sector_code": "INDUS"},
]

FUNDS = [
    {"symbol": "KT-WTAI-A",  "name_th": "กรุงไทย World AI and Technology",  "sector_code": "FUND_GLOBAL"},
    {"symbol": "KFLTFDIV-A", "name_th": "กรุงศรี LTF หุ้นปันผล",            "sector_code": "FUND_EQUITY"},
    {"symbol": "TMBGQG",     "name_th": "ทหารไทย Global Quality Growth",      "sector_code": "FUND_GLOBAL"},
    {"symbol": "SCBDV",      "name_th": "ไทยพาณิชย์หุ้นระยะยาว ปันผล",       "sector_code": "FUND_EQUITY"},
    {"symbol": "KT-GOVBOND", "name_th": "กรุงไทย ตราสารหนี้รัฐบาล",          "sector_code": "FUND_FIXED"},
    {"symbol": "KFRMUL-A",   "name_th": "กรุงศรี REIT และ Infra",             "sector_code": "FUND_REIT"},
]

FOREX = [
    {"symbol": "USD/THB", "name_th": "ดอลลาร์สหรัฐ / บาทไทย",  "sector_code": "FX_ASIA",
     "metadata": {"base": "USD", "quote": "THB"}},
    {"symbol": "EUR/THB", "name_th": "ยูโร / บาทไทย",           "sector_code": "FX_MAJOR",
     "metadata": {"base": "EUR", "quote": "THB"}},
    {"symbol": "JPY/THB", "name_th": "เยนญี่ปุ่น / บาทไทย",    "sector_code": "FX_ASIA",
     "metadata": {"base": "JPY", "quote": "THB"}},
    {"symbol": "CNY/THB", "name_th": "หยวนจีน / บาทไทย",       "sector_code": "FX_ASIA",
     "metadata": {"base": "CNY", "quote": "THB"}},
    {"symbol": "EUR/USD", "name_th": "ยูโร / ดอลลาร์สหรัฐ",    "sector_code": "FX_MAJOR",
     "metadata": {"base": "EUR", "quote": "USD"}},
    {"symbol": "GBP/USD", "name_th": "ปอนด์อังกฤษ / ดอลลาร์",  "sector_code": "FX_MAJOR",
     "metadata": {"base": "GBP", "quote": "USD"}},
]


def seed():
    db = get_supabase()

    stock_rows = [{"symbol": s["symbol"], "name_th": s["name_th"],
                   "asset_type": "STOCK", "sector_code": s["sector_code"]} for s in STOCKS]
    fund_rows  = [{"symbol": f["symbol"], "name_th": f["name_th"],
                   "asset_type": "FUND",  "sector_code": f["sector_code"]} for f in FUNDS]
    forex_rows = [{"symbol": x["symbol"], "name_th": x["name_th"],
                   "asset_type": "FOREX", "sector_code": x["sector_code"],
                   "metadata": x.get("metadata", {})} for x in FOREX]

    all_rows = stock_rows + fund_rows + forex_rows
    db.table("assets").upsert(all_rows, on_conflict="symbol").execute()

    print(f"✅ Seeded {len(STOCKS)} stocks, {len(FUNDS)} funds, {len(FOREX)} forex pairs")
    print(f"   Total: {len(all_rows)} assets")


if __name__ == "__main__":
    seed()
