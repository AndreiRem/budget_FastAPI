from schemas import STransactionAdd, STransaction, STransactionId
from repository import TransactionRepository
from typing import Annotated
from fastapi import Depends, APIRouter


router = APIRouter(
    prefix='/transactions',
    tags=['Transactions']
)


@router.get('')
async def get_transactions() -> list[STransaction]:
    transactions = await TransactionRepository.find_all()
    return transactions


@router.post('')
async def add_transaction(transaction: Annotated[STransactionAdd, Depends()]) -> STransactionId:
    transaction_id = await TransactionRepository.add_one(transaction)
    return STransactionId(transaction_id=transaction_id)
