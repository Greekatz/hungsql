import json
from pathlib import Path

CREDENTIALS_FILE = Path(__file__).resolve().parents[2] / "key" / "credentials.json"

class UserRepository:
    def __init__(self):
        self.users = self._load_users()

    def _load_users(self):
        with open(CREDENTIALS_FILE, "r") as f:
            return json.load(f)

    def get_user_by_email(self, email: str):
        return next((user for user in self.users if user["email"] == email), None)