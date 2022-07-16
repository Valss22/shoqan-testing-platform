from time import time
from typing import Union
import bcrypt
import jwt
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist
from src.static.emails import admin_emails
from src.settings import TOKEN_KEY, TOKEN_TIME
from src.user.model import User
from src.user.schemas import UserIn


class UserService:

    async def create_user(self, user: UserIn):
        password = user.dict()["password"]
        email: EmailStr = user.dict()["email"]

        if await User.filter(email=email):
            return JSONResponse({
                "detail": "Данный пользователь уже существует"
            }, status.HTTP_400_BAD_REQUEST)

        password = password.encode()
        await User.create(**user.dict(), password_hash=password)

    async def auth_user(self, user: UserIn) -> Union[None, dict, JSONResponse]:
        email: EmailStr = user.dict()["email"]
        is_admin: bool = email in admin_emails

        password: bytes = user.dict()["password"].encode()
        try:
            current_user = await User.get(email=email)
        except DoesNotExist:
            return JSONResponse(
                {"detail": "Данного пользователя не существует"},
                status.HTTP_400_BAD_REQUEST
            )

        if bcrypt.checkpw(password, current_user.password_hash):
            payload: dict = {
                "id": str(current_user.id),
                "email": current_user.email,
                "isAdmin": is_admin,
                "exp": time() + TOKEN_TIME
            }
            return {
                **current_user.__dict__,
                "token": jwt.encode(payload, TOKEN_KEY),
                "isAdmin": is_admin,
            }
        return JSONResponse(
            {"detail": "Неверный пароль"},
            status.HTTP_400_BAD_REQUEST
        )
