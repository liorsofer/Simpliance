from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/address", tags=["address"])


@router.get("/{bitcoin_address}")
async def get_balance_and_transaction_count(bitcoin_address: str):
    return {bitcoin_address: "get_balance_and_transaction_count details"}
