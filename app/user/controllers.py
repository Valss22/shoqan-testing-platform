from fastapi import APIRouter, Depends
from app.user.schemas import UserIn
from app.user.service import UserService

user_router = APIRouter()


@user_router.post('/user/register/')
async def register_user(user_in: UserIn, user_service: UserService = Depends()):
    await user_service.create_user(user_in)
