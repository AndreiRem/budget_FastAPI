from pydantic import BaseModel


class STransactionAdd(BaseModel):
    amount: float
    description: str | None


class STransaction(STransactionAdd):
    id: int


class STransactionId(BaseModel):
    ok: bool = True
    transaction_id: int
