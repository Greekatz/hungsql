from fastapi import APIRouter
from hungsql.auth.schemas.user import UserCreate, UserOut
from hungsql.auth.services.user_service import UserService

router = APIRouter(prefix="/v1/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def register(user: UserCreate):
    return await UserService().create_user(user)