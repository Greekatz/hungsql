import json
from pathlib import Path
from typing import Optional
from hungsql.auth.schemas.user import UserCreate, UserOut

CREDENTIALS_FILE = Path(__file__).resolve().parents[2] / "key" / "credentials.json"

class UserRepository:
    def _load_users(self):
        if CREDENTIALS_FILE.exists():
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        return []

    def _save_users(self, users):
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(users, f, indent=2)

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        return next((u for u in self._load_users() if u["email"] == email), None)

    async def get_user_by_username(self, username: str) -> Optional[dict]:
        return next((u for u in self._load_users() if u["username"] == username), None)

    async def create_user(self, payload: UserCreate) -> UserOut:
        user_dict = payload.model_dump()
        users = self._load_users()
        users.append(user_dict)
        self._save_users(users)
        return UserOut(**user_dict)