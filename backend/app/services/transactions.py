from app.db.repositories.transactions import TransactionRepository
from app.schemas.transactions import TransactionBase, TransactionUpdate, TransactionCreate
from app.schemas.users import UserResponse
from app.services.base import get_service_factory


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def create_transaction(self, transaction: TransactionBase, current_user: UserResponse):
        transaction = transaction.model_dump()
        transaction["user_id"] = current_user.id
        transaction_create = TransactionCreate(**transaction)
        return await self.repository.create(transaction_create)

    async def get_all_transactions(self):
        return await self.repository.get_all()

    async def get_transaction_by_id(self, transaction_id: int):
        return await self.repository.get_by_id(transaction_id)

    async def update_transaction(self, transaction_id: int, transaction_data: TransactionUpdate):
        return await self.repository.update(transaction_id, transaction_data)

    async def delete_transaction(self, transaction_id: int):
        return await self.repository.delete(transaction_id)


get_transaction_service = get_service_factory(TransactionRepository, TransactionService)
