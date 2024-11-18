from app.db.repositories.transactions import TransactionRepository
from app.schemas.transactions import TransactionCreate, TransactionUpdate


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def create_transaction(self, transaction_data: TransactionCreate):
        return await self.repository.create(transaction_data)

    async def get_all_transactions(self):
        return await self.repository.get_all()

    async def get_transaction_by_id(self, transaction_id: int):
        return await self.repository.get_by_id(transaction_id)

    async def update_transaction(self, transaction_id: int, transaction_data: TransactionUpdate):
        return await self.repository.update(transaction_id, transaction_data)

    async def delete_transaction(self, transaction_id: int):
        return await self.repository.delete(transaction_id)