
from fastapi import APIRouter

from hungsql.server.schemas.query import QueryRequest, QueryResponse
from hungsql.server.services.query_service import QueryService

router = APIRouter(prefix="/v1/query", tags=["query"])
service = QueryService()


@router.post("/one", response_model=QueryResponse)
def fetch_one(request: QueryRequest):
    return service.fetch_one(token=request.token, sql=request.sql, dsn=request.dsn)

@router.post("/many", response_model=QueryResponse)
def fetch_many(request: QueryRequest):
    return service.fetch_many(token=request.token, sql=request.sql, dsn=request.dsn)

@router.post("/all", response_model=QueryResponse)
def fetch_all(request: QueryRequest):
    return service.fetch_all(token=request.token, sql=request.sql, dsn=request.dsn)