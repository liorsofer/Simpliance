from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.get("/{transaction_hash}")
async def get_transaction_details(transaction_hash: str):
    return {transaction_hash: "transaction details"}
