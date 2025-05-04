from typing import Any, List, Tuple
from pydantic import BaseModel

class QueryRequest(BaseModel):
    token: str
    sql: str
    dsn: str

class QueryResponse(BaseModel):
    data: List[Tuple[Any, ...]]
    rowcount: int
    description: List[Tuple[str, Any, Any, Any, Any, Any, Any]]