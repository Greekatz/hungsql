from fastapi import HTTPException
from dbcsv.server.services.auth_service import AuthService
from dbcsv.client.dbapi2.connection import Connection

def connect(dsn: str, username: str, password: str) -> Connection:
    try:
        token = AuthService().sync_authenticate_user(email=username, password=password)
        return Connection(user_email=username, token=token.access_token, dsn=dsn)
    except HTTPException as e:
        raise PermissionError("Invalid credentials") from e
