from pydantic import BaseModel
from typing import List


class Input(BaseModel):
    address: str
    value: int


class Output(BaseModel):
    address: str
    value: int


class BitcoinTransaction(BaseModel):
    hash: str
    fee: int
    inputs: List[Input]
    outputs: List[Output]
    transaction_index: int
    block_time: int
