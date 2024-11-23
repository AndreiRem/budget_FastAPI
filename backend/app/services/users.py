from app.db.models import UserORM
from app.schemas.users import UserCreate, UserResponse
from app.core.security import verify_password
from app.db.repositories.users import UserRepository
from app.core.jwt import decode_access_token
from jwt.exceptions import InvalidTokenError


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