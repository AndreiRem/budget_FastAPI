from app.schemas.users import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import get_password_hash
from app.db.models import UserORM


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username) -> UserORM | None:
        user = await (self.db.execute(select(UserORM).filter(UserORM.username == username)))
        return user.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> UserORM:
        hashed_password = get_password_hash(user_data.password)
        db_user = UserORM(username=user_data.username, hashed_password=hashed_password)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
