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
    user_id: int


class TransactionUpdate(TransactionCreate):
    pass


class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_attributes = True
