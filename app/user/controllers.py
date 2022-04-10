from fastapi import APIRouter, Depends

from app.decorators.is_admin import is_admin
from app.user.schemas import UserIn, UserOut
from app.user.service import UserService

user_router = APIRouter(
    prefix='/user'
)


@user_router.post('/register/')
async def register_user(user_in: UserIn, user_service: UserService = Depends()):
    return await user_service.create_user(user_in)


@user_router.post('/login/', response_model=UserOut)
@is_admin
async def login_user(user_in: UserIn, user_service: UserService = Depends()):
    pass
