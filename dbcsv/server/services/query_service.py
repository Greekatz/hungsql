from fastapi import HTTPException, status

from dbcsv.client.dbapi2.connection import Connection
from dbcsv.server.utils.token import verify_token


class QueryService:
    def _get_cursor(self, token: str, sql: str, dsn: str):
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
        return cursor

    def fetch_one(self, token: str, sql: str, dsn: str):
        cursor = self._get_cursor(token, sql, dsn)
        result = cursor.fetchone()
        description = cursor.description
        cursor.close()
        return {
            "data": [result] if result else [],
            "rowcount": 1 if result else 0,
            "description": description
        }

    def fetch_many(self, token: str, sql: str, dsn: str):
        cursor = self._get_cursor(token, sql, dsn)
        results = cursor.fetchmany()
        description = cursor.description
        rowcount = len(results)
        cursor.close()
        return {
            "data": results,
            "rowcount": rowcount,
            "description": description
        }

    def fetch_all(self, token: str, sql: str, dsn: str):
        cursor = self._get_cursor(token, sql, dsn)
        results = cursor.fetchall()
        description = cursor.description
        rowcount = len(results)
        cursor.close()
        return {
            "data": results,
            "rowcount": rowcount,
            "description": description
        }
