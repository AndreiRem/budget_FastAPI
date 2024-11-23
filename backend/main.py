from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.endpoints.transaction import router as transactions_router
from app.api.endpoints.user import router as users_router
from app.db.session import drop_tables, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_tables()
    # print('Old database cleaned')
    # await create_tables()
    # print('New database created')
    yield
    print('Ready to work')


app = FastAPI(lifespan=lifespan)
app.include_router(transactions_router)
app.include_router(users_router)
