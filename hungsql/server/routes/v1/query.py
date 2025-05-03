import traceback
from fastapi import APIRouter, HTTPException
from hungsql.server.schemas.query import QueryRequest, QueryResponse
from hungsql.server.services.query_service import QueryService

router = APIRouter(prefix="/v1/query", tags=["query"])
service = QueryService()

@router.post("/", response_model=QueryResponse)
def run_query(request: QueryRequest):
    try:
        return service.execute_sql(token=request.token, sql=request.sql, dsn=request.dsn)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))