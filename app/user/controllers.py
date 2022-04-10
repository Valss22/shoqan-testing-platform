from fastapi import APIRouter, Depends
from app.user.schemas import UserIn, UserOut
from app.user.service import UserService

user_router = APIRouter(
    prefix='/user'
)


@user_router.post('/register/')
async def register_user(user_in: UserIn, user_service: UserService = Depends()):
    return await user_service.create_user(user_in)


@user_router.post('/login/', response_model=UserOut)
async def login_user(user_in: UserIn, user_service: UserService = Depends()):
    return await user_service.auth_user(user_in)
