from app.db.models import UserORM
from app.schemas.user import UserCreate, UserResponse
from app.core.security import verify_password
from app.db.repositories.user import UserRepository
from app.core.jwt import decode_access_token
from jwt.exceptions import InvalidTokenError
from app.services.base import get_service_factory
from fastapi import Depends, HTTPException, status
from app.schemas.user import UserId
from app.core.security import oauth2_scheme


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_username(self, username: str) -> UserORM | None:
        return await self.repository.get_by_username(username)

    async def authenticate_user(self, username: str, password: str) -> UserResponse | None:
        user = await self.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def create_user(self, user_data: UserCreate) -> UserResponse | None:
        return await self.repository.create(user_data)

    async def get_user_from_token(self, token: str) -> UserResponse:
        try:
            payload = decode_access_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise ValueError("Invalid token: username is missing")
            user = await self.repository.get_by_username(username)
            if user is None:
                raise ValueError("User not found")
            return user
        except InvalidTokenError:
            raise ValueError("Invalid token")


get_user_service = get_service_factory(UserRepository, UserService)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> UserId:
    try:
        user = await user_service.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized"
            )
        return UserId(id=user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
