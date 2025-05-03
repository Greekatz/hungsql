import pytest
from fastapi import HTTPException

from hungsql.auth.services.auth_service import AuthService
from hungsql.auth.schemas.token import Token

# These must match an entry in key/credentials.json
TEST_EMAIL = "user231@example.com"
TEST_PASSWORD = "SecurePass123123"
WRONG_PASSWORD = "wrongpass"

@pytest.mark.asyncio
async def test_successful_authentication():
    auth_service = AuthService()
    token: Token = await auth_service.authenticate_user(
        email=TEST_EMAIL, password=TEST_PASSWORD
    )

    assert token.access_token is not None
    assert token.refresh_token is not None
    assert token.token_type == "bearer"

@pytest.mark.asyncio
async def test_authentication_failure_wrong_password():
    auth_service = AuthService()

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.authenticate_user(
            email=TEST_EMAIL, password=WRONG_PASSWORD
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"

@pytest.mark.asyncio
async def test_authentication_failure_unknown_user():
    auth_service = AuthService()

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.authenticate_user(
            email="no@user.com", password="any"
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"
