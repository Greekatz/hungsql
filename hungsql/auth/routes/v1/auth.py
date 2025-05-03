from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from hungsql.auth.schemas.token import Token
from hungsql.auth.services.auth_service import AuthService

router = APIRouter(prefix="/v1/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    auth = AuthService()  
    return await auth.authenticate_user(email=form.username, password=form.password)


