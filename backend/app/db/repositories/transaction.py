from typing import Sequence
from sqlalchemy.future import select
from app.db.models import TransactionORM
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.schemas.user import UserId


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, transaction_data: TransactionCreate) -> TransactionORM:
        transaction = TransactionORM(**transaction_data.model_dump())
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def get_all(self, user_id: UserId) -> Sequence[TransactionORM]:
        result = await self.db.execute(select(TransactionORM).filter(TransactionORM.user_id == user_id.id))
        return result.scalars().all()

    async def get_by_id(self, transaction_id: int) -> TransactionORM | None:
        result = await self.db.execute(select(TransactionORM).where(TransactionORM.id == transaction_id))
        return result.scalar_one_or_none()

    async def update(self, transaction_id: int, transaction_data: TransactionUpdate) -> TransactionORM | None:
        transaction = await self.get_by_id(transaction_id)
        if not transaction:
            return None
        for key, value in transaction_data.model_dump(exclude_unset=True).items():
            setattr(transaction, key, value)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def delete(self, transaction_id: int) -> bool:
        transaction = await self.get_by_id(transaction_id)
        if not transaction:
            return False
        await self.db.delete(transaction)
        await self.db.commit()
        return True
