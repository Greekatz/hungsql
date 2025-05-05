from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from dbcsv.server.schemas.token import Token
from dbcsv.server.services.auth_service import AuthService

router = APIRouter(prefix="/v1/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    auth = AuthService()  
    return await auth.authenticate_user(email=form.username, password=form.password)


