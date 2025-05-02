# app/services/auth_service.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from hungsql.auth.hashing import Hash
from hungsql.auth.utils.token import create_access_token, create_refresh_token
from hungsql.auth.repositories.user import UserRepository
from hungsql.auth.schemas.token import Token


class AuthService:
    """Business logic for authentication."""

    def __init__(self):
        # one repository per service keeps concerns clean
        self.user_repo = UserRepository()

    async def authenticate_user(self, *, email: str, password: str) -> Token:
        """
        Validate user credentials and return access + refresh JWTs.

        Raises:
            HTTPException 401 – if user not found or password mismatch.
        """
        user = self.user_repo.get_user_by_email(email)
        if not user or not Hash.verify(user["password"], password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token  = create_access_token ({"sub": user["email"]})
        refresh_token = create_refresh_token({"sub": user["email"]})

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
