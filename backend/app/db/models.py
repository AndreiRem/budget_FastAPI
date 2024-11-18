from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class TransactionORM(Base):
    __tablename__ = 'transaction'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    description: Mapped[str | None]
