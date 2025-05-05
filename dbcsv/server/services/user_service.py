from datetime import datetime, timezone
from fastapi import HTTPException, status

from dbcsv.server.hashing import Hash
from dbcsv.server.repositories.user_repository import UserRepository
from dbcsv.server.schemas.user import UserCreate, UserOut


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def _generate_user_id(self):
        users = self.user_repo._load_users()
        return max((u.get("id", 0) for u in users), default=0) + 1

    async def create_user(self, payload: UserCreate) -> UserOut:
        if await self.user_repo.get_user_by_email(payload.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        if await self.user_repo.get_user_by_username(payload.username):
            raise HTTPException(status_code=400, detail="Username already taken")

        user_data = payload.model_copy(update={
            "hashed_password": Hash.bcrypt(payload.password),
            "created_at": datetime.now(timezone.utc),
            "is_active": True,
            "id": self._generate_user_id()

        })

        return await self.user_repo.create_user(user_data)