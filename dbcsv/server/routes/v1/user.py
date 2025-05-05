from fastapi import APIRouter
from dbcsv.server.schemas.user import UserCreate, UserOut
from dbcsv.server.services.user_service import UserService

router = APIRouter(prefix="/v1/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def register(user: UserCreate):
    return await UserService().create_user(user)