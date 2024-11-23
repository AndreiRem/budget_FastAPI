from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.jwt import create_access_token
from app.services.users import UserService
from app.schemas.users import UserCreate, UserResponse, Token
from app.db.repositories.users import UserRepository
from typing import Annotated
from app.core.security import oauth2_scheme


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


def get_service(db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    return UserService(repository)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_service)):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_access_token({"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, service: UserService = Depends(get_service)):
    return await service.create_user(user_data)


@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route"}


@router.get("/me", response_model=UserResponse)
async def get_user(token: Annotated[str, Depends(oauth2_scheme)],
                   service: UserService = Depends(get_service)):
    user = await service.get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or user not found",
        )
    return user
