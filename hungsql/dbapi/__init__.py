from fastapi import HTTPException
from hungsql.auth.services.auth_service import AuthService
from hungsql.dbapi.connection import Connection

def connect(dsn: str, user: str, password: str) -> Connection:
    try:
        token = AuthService().sync_authenticate_user(email=user, password=password)
        return Connection(user_email=user, token=token.access_token, dsn=dsn)
    except HTTPException as e:
        raise PermissionError("Invalid credentials") from e
