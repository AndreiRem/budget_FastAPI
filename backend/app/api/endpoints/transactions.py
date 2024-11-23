from fastapi import APIRouter, Depends, HTTPException
from app.services.transactions import TransactionService
from app.schemas.transactions import TransactionBase, TransactionUpdate, TransactionResponse
from app.services.transactions import get_transaction_service
from app.schemas.users import UserResponse
from app.services.users import get_current_user


router = APIRouter(
    prefix='/transactions',
    tags=['Transactions']
)


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionBase,
    current_user: UserResponse = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.create_transaction(transaction, current_user)


@router.get("/", response_model=list[TransactionResponse])
async def get_all_transactions(
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_all_transactions()


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service)
):
    transaction = await service.get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    service: TransactionService = Depends(get_transaction_service)
):
    updated_transaction = await service.update_transaction(transaction_id, transaction)
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service)
):
    success = await service.delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted successfully"}
