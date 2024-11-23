from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.db.session import Base


class TransactionORM(Base):
    __tablename__ = 'transaction'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    description: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, default=1)


class UserORM(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
