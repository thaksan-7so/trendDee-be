from fastapi import APIRouter
from app.models.portfolio import TransactionCreate
from app.core.supabase import get_supabase
from app.services.portfolio_service import get_portfolio_summary

router = APIRouter()


@router.get("/summary")
async def portfolio_summary():
    return await get_portfolio_summary()


@router.get("/transactions")
def list_transactions():
    db = get_supabase()
    return db.table("portfolio_transactions").select("*").order("transaction_date", desc=True).execute().data


@router.post("/transactions")
def add_transaction(tx: TransactionCreate):
    db = get_supabase()
    return db.table("portfolio_transactions").insert(tx.model_dump()).execute().data[0]


@router.delete("/transactions/{tx_id}")
def delete_transaction(tx_id: str):
    db = get_supabase()
    db.table("portfolio_transactions").delete().eq("id", tx_id).execute()
    return {"deleted": tx_id}
