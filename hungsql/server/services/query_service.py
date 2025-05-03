from fastapi import HTTPException, status

from hungsql.dbapi.connection import Connection
from hungsql.server.utils.token import verify_token


class QueryService:
    def execute_sql(self, token: str, sql: str, dsn: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

        user = verify_token(token, credentials_exception=credentials_exception)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        conn = Connection(dsn=dsn, user_email=user.email)
        cursor = conn.cursor()
        cursor.execute(sql)
        return {
            "data": cursor.fetchmany(),
            "rowcount": cursor.rowcount,
            "description": cursor.description
        }
