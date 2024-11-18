from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
# from dotenv import load_dotenv


class Base(DeclarativeBase):
    pass

# load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite+aiosqlite:///transactions.db')

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_sessionmaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_sessionmaker() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)