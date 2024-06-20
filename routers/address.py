from fastapi import APIRouter, HTTPException
from requests import HTTPError

from models.bitcoin_address import BitcoinAddress
from services.address import get_bitcoin_address_info

router = APIRouter(prefix="/address", tags=["address"])


@router.get("/{bitcoin_address}", response_model=BitcoinAddress)
async def get_balance_and_transaction_count(bitcoin_address: str) -> BitcoinAddress:
    try:
        data = get_bitcoin_address_info(bitcoin_address)
        if not data:
            raise HTTPException(status_code=404, detail="Bitcoin address not found")
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
