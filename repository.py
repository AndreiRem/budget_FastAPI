from database import new_session, TransactionORM
from schemas import STransactionAdd, STransaction
from sqlalchemy import select


class TransactionRepository:
    @classmethod
    async def add_one(cls, data: STransactionAdd) -> int:
        async with new_session() as session:
            transaction_dict = data.model_dump()
            print(transaction_dict)
            transaction = TransactionORM(**transaction_dict)
            session.add(transaction)
            await session.flush()
            await session.commit()
            return transaction.id

    @classmethod
    async def find_all(cls) -> list[STransaction]:
        async with new_session() as session:
            query = select(TransactionORM)
            result = await session.execute(query)
            transaction_models = result.scalars().all()
            transaction_schemas = [STransaction.model_validate(model) for model in transaction_models]
            return transaction_schemas
