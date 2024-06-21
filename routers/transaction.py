from fastapi import APIRouter, HTTPException
from requests import HTTPError

from models.bitcoin_transaction import BitcoinTransaction
from services.transcation import get_transaction_info

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.get("/{transaction_hash}", response_model=BitcoinTransaction)
async def get_transaction_details(transaction_hash: str) -> BitcoinTransaction:
    try:
        data = get_transaction_info(transaction_hash)
        if not data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error, {str(e)}")
