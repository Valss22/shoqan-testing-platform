from time import time
from typing import Union, Optional

import bcrypt
import jwt
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist

from src.email_sender.service import email_sender_service
from src.static.emails import admin_emails
from src.settings import TOKEN_KEY, TOKEN_TIME
from src.user.model import User
from src.user.schemas import UserIn
import secrets


class UserService:
    def __init__(self):
        self.email_sender_service = email_sender_service

    async def create_user(self, user: UserIn) -> Optional[JSONResponse]:
        password: Union[str, bytes] = secrets.token_urlsafe(4)
        email: EmailStr = user.dict()["email"]

        if await User.filter(email=email):
            return JSONResponse({
                "detail": "Данный пользователь уже существует"
            }, status.HTTP_400_BAD_REQUEST)

        # self.send_password_to_email(password, email)
        self.email_sender_service.send_password(password, email)
        password = password.encode()
        await User.create(**user.dict(), password_hash=password)

    # def send_password_to_email(self, password: str, email: EmailStr) -> None:
    #     smtp = smtplib.SMTP("smtp.gmail.com", 587)
    #     smtp.starttls()
    #     smtp.login("ShoqanPlatform@gmail.com", "mLq-8eS-NAA-S9T")
    #     smtp.sendmail("ShoqanPlatform@gmail.com", [email], password)
    #     smtp.quit()

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
