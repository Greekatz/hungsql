from fastapi import FastAPI

from hungsql.server.routes.v1.auth import router as auth_router
from hungsql.server.routes.v1.user import router as user_router
from hungsql.server.routes.v1.query import router as query_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(query_router)

@app.get("/")
def root():
    return {"message": "HungSQL API is alive"}
