from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.repositories.transactions import TransactionRepository
from app.services.transactions import TransactionService
from app.schemas.transactions import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter(
    prefix='/transactions',
    tags=['Transactions']
)


def get_service(db: AsyncSession = Depends(get_db)):
    repository = TransactionRepository(db)
    return TransactionService(repository)


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate, service: TransactionService = Depends(get_service)
):
    return await service.create_transaction(transaction)


@router.get("/", response_model=list[TransactionResponse])
async def get_all_transactions(service: TransactionService = Depends(get_service)):
    return await service.get_all_transactions()


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, service: TransactionService = Depends(get_service)):
    transaction = await service.get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int, transaction: TransactionUpdate, service: TransactionService = Depends(get_service)
):
    updated_transaction = await service.update_transaction(transaction_id, transaction)
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int, service: TransactionService = Depends(get_service)):
    success = await service.delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted successfully"}
