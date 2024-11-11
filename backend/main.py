from fastapi import FastAPI
from backend.database import create_tables, delete_tables
from contextlib import asynccontextmanager
from router import router as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('Old database cleaned')
    await create_tables()
    print('New database created')
    yield
    print('Ready to work')

app = FastAPI(lifespan=lifespan)
app.include_router(transactions_router)