from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class TransactionBase(BaseModel):
    amount: float
    description: Annotated[str | None, Field(
        max_length=200,
        description="Description of transaction",
        title="Title of transaction",
        default=None)]


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True
