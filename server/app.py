from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from server.dbengine import DatabaseEngine

app = FastAPI()
security = HTTPBasic()

VALID_USER = "admin"
VALID_PASS = "1234"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != VALID_USER or credentials.password != VALID_PASS:
        raise HTTPException(status_code=401, detail="Unauthenticated Access")
    return credentials.username


@app.post("/query")
async def run_query(request: Request, username: str = Depends(authenticate)):
    try:
        data = await request.json()
        print(f"Received data: {data}")  # Debug input
        query = data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter missing")
        
        result = DatabaseEngine().execute_query(query)
        return result
    except ValueError as e:
        print(f"SQL Error: {e}")  
        raise HTTPException(status_code=400, detail=str(e))
    


    