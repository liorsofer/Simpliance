from pydantic import BaseModel


class BitcoinAddress(BaseModel):
    address: str
    balance: int
    transaction_count: int
