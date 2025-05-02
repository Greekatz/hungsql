from datetime import datetime, timezone
from fastapi import HTTPException, status

from hungsql.auth.hashing import Hash
from hungsql.auth.repositories.user_repository import UserRepository
from hungsql.auth.schemas.user import UserCreate, UserOut


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def create_user(self, payload: UserCreate) -> UserOut:
        if await self.user_repo.get_user_by_email(payload.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        if await self.user_repo.get_user_by_username(payload.username):
            raise HTTPException(status_code=400, detail="Username already taken")

        user_data = payload.model_copy(update={
            "password": Hash.bcrypt(payload.password),
            "created_at": datetime.now(timezone.utc)
        })

        return await self.user_repo.create_user(user_data)