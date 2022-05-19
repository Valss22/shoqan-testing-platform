from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from src.email_sender.service import email_sender_service
from src.user.schemas import UserIn, UserOut
from src.user.service import UserService

user_router = APIRouter(
    prefix="/user"
)


@user_router.post("/register/")
async def register_user(
    user: UserIn, background_tasks: BackgroundTasks,
    user_service: UserService = Depends()
):
    return await user_service.create_user(user, background_tasks)


@user_router.post("/login/", response_model=UserOut)
async def login_user(
    user: UserIn,
    user_service: UserService = Depends()
):
    return await user_service.auth_user(user)


# @user_router.get("/background/")
# async def test_task(
#     background_tasks: BackgroundTasks,
# ):
#     background_tasks.add_task(email_sender_service.send_password, "1234", "valsshokorov@gmail.com")
#     return {"msg": "ok"}
